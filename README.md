### Delivery Service Web App

This project is built using FastAPI (Python), Redis (DB and Cache) on the backend, and React, Bootstrap for the frontend.

This is a simulation of the events that occur during a delivery service from the time of order starts to the delivery of the order.

The purpose of this project is to visualize the event-driven architecture using an application.

### Events

1. Set Budget, notes - this will set the order, aka status will be ready
2. Once the order is ready, then the courier will make the order active by starting the order
3. The courier then picks up the order, changing the status to collected
4. Finally, the courier delivers the order, closing the order and status becomes completed.

### How to run this project

1. Clone the project to your local machine
2. Open the project in Vscode or any text editor and open two terminals
3. `cd frontend` and run `npm start` to run the frontend in the first terminal
4. `cd backend` and run `uvicorn app:main --reload` to start the server in the second terminal
5. Enjoy!
