# App Builder’s Workshop

A beginner-friendly, hands-on course for understanding how a Tauri desktop app can connect a React interface to application logic and persistent data. It is designed for learners who know a little Python and want to build up to a small, working app feature.

The main course has 11 expanded chapters. A separate folder preserves the earlier concise versions, and an optional Python course goes deeper into backend automation.

## Choose a learning path

- **[Expanded course](index.html)** — the recommended path, with detailed explanations, examples, exercises, and worked answers.
- **[Concise chapters](short-chapters/index.html)** — shorter versions for a quick overview or review. Each chapter links to its expanded counterpart.
- **[Python Backend & Automation course](python-course/index.html)** — a separate 15-lesson course about Python application logic, scripting, APIs, queues, and deployment.

Chapter completion and theme preferences are stored in your browser. Progress is specific to a browser and site address, so it does not automatically transfer between your local copy and a hosted site.

## Main course: chapter overview

1. **[Map the app before writing code](chapters/01-app-map.html)**  
   Learn how the interface, application logic, backend, and database fit together. Trace a task through the system, define a shared data contract, and compare a FastAPI sidecar with direct Tauri/Rust commands.

2. **[HTML, CSS, and the browser](chapters/02-html-css.html)**  
   Learn how a browser interprets a page, build a semantic task form, and apply layout, responsive design, and accessibility basics.

3. **[JavaScript values and data structures](chapters/03-js-data.html)**  
   Work with `const`, `let`, primitive values, objects, arrays, references, `null`, and `undefined`. Model app records and understand which data can safely travel as JSON.

4. **[Decisions, functions, and useful array methods](chapters/04-js-logic.html)**  
   Use conditions, ordinary and arrow functions, and array methods to express application rules. Practice validating user input and transforming lists.

5. **[Async JavaScript, HTTP, and JSON](chapters/05-async-json.html)**  
   Learn how `async`/`await`, Promises, HTTP requests, and JSON work together. Handle loading and error cases, and understand the development proxy and CORS.

6. **[React components, JSX, props, and events](chapters/06-react-components.html)**  
   Break an interface into components, pass data with props, and connect user actions to event handlers.

7. **[React state, forms, and data-driven screens](chapters/07-react-state.html)**  
   Manage form input and server data with state. Use immutable updates and show distinct loading, empty, success, and error states.

8. **[Python refresh and FastAPI endpoints](chapters/08-python-fastapi.html)**  
   Apply familiar Python concepts to request models, validation, business logic, and CRUD endpoints. Learn how the frontend and backend agree on data and errors.

9. **[SQL and SQLite: persistent records](chapters/09-sqlite.html)**  
   Create tables and relationships, query and update data safely, use parameterized SQL and transactions, and consider persistence and schema changes.

10. **[Tauri, Rust, and the desktop boundary](chapters/10-tauri-rust.html)**  
    Understand the Tauri v2 desktop architecture, Rust commands, capabilities, permissions, and packaging. Compare using Rust for local operations with running FastAPI as a separate service.

11. **[Capstone: build one complete feature](chapters/11-capstone.html)**  
    Bring the course together in a task-tracker vertical slice: a user enters a task, the app validates and saves it, and the saved record appears in the interface.

## Capstone overview

The capstone teaches you to plan and connect one useful feature across the UI, API, and database. Its example record is a task with an integer ID, a trimmed title, a completion status, and a UTC creation timestamp.

The example API contract covers:

- `GET /tasks` to list tasks
- `POST /tasks` to create one
- `PATCH /tasks/{id}` to update completion status
- `DELETE /tasks/{id}` to delete one
- `404` for a missing task and `422` for invalid input

You also work through UI loading, empty, saving, and error states; SQLite persistence; basic testing; and reviewing generated code. The task example can later be adapted to products, bookings, stock movements, or another business workflow.

**Architecture note:** The course is educational material, not a finished Tauri application. It explains two distinct integration choices: a FastAPI service/sidecar or direct Tauri/Rust commands. A packaged FastAPI sidecar needs additional work for process lifecycle, local networking, permissions, and packaging. React should not connect directly to SQLite.

## Run it online

Use the Github Pages like in the about section.

## Run the course website locally

You only need Python 3 to serve the static course pages. No Node.js, Rust, database, or build step is required just to read the website.

1. Clone or download the repository, or unzip the course bundle.
2. Open a terminal in the project’s root folder—the folder containing `index.html`.
3. Start a local static web server:

   ```bash
   python3 -m http.server 8000 --bind 127.0.0.1
   ```

   On Windows, you can use:

   ```powershell
   py -m http.server 8000 --bind 127.0.0.1
   ```

4. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/ ) in your browser.
5. Stop the server with **Ctrl+C** in the terminal.

Use the local web address instead of opening `index.html` directly. Serving the files over HTTP makes navigation and browser-based progress behave consistently.

## Tools for practising the lessons

You can read the course without installing development tools. For the coding exercises, the recommended tools are:

- A code editor, such as Visual Studio Code
- A current Node.js LTS release
- Python 3
- Git and a terminal
- Rust via `rustup` when you reach the Tauri chapter
- SQLite command-line tools, if desired

Install tools as you reach the relevant lessons rather than trying to set up the entire stack at the start. The course is a learning path and build guide; it does not include a completed, runnable capstone app.

