import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
import consumer



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-12322.c258.us-east-1-4.ec2.cloud.redislabs.com",
    port=12322,
    password="5ZwoDiAFCGmtfcDVpvzuzvtOpo99UFXF",
    decode_responses=True
)


class Delivery(HashModel):

    budget: int = 0
    notes: str = ""

    class Meta:
        database = redis


class Event(HashModel):

    delivery_id: str = None
    event_type: str
    data: str

    class Meta:
        database = redis

@app.get('/deliveries/{pk}/status')
async def get_state(pk: str):
    state = redis.get(f'delivery: {pk}')

    return json.loads(state) if state is not None else build_state(pk)


def build_state(pk: str):
    """
    Builds the state manually if redis is not available
    """
    pks = Event.all_pks()
    all_events = [Event.get(pk) for pk in pks]
    events = [event for event in all_events if event.delivery_id == pk]
    state = {}
    for event in events:
        state = consumer.CONSUMERS[event.event_type](state, event)

    return state

@app.post('/deliveries/create')
async def create(request: Request):
    body = await request.json()
    delivery = Delivery(budget=body['data']['budget'], notes=body['data']['notes'])
    event = Event(delivery_id=delivery.pk, event_type=body['type'], data=json.dumps(body['data'])).save()
    state = consumer.CONSUMERS[event.event_type]({}, event)
    redis.set(f'delivery: {delivery.pk}', json.dumps(state)) # storing state in cache
    return state

@app.post('/event')
async def dispatch(request: Request):
    body = await request.json()
    delivery_id = body['delivery_id']
    event = Event(delivery_id=delivery_id, event_type=body['event_type'], data=json.dumps(body['data'])).save()
    state = await get_state(delivery_id)
    new_state = consumer.CONSUMERS[event.event_type](state, event)
    redis.set(f'delivery: {delivery_id}', json.dumps(new_state))
    return new_state