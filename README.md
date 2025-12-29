TASK MANAGEMENT SYSTEM
=====================

Author: Aryan Bhatia
Tech Stack:
- Frontend: React.js
- Backend: FastAPI (Python)
- Database: MySQL
- Auth: JWT (JSON Web Tokens)

--------------------------------------------------
PROJECT OVERVIEW
--------------------------------------------------
This is a role-based Task Management System where users can log in,
admins can assign and manage tasks, and users can view tasks assigned
to them. Authentication is handled using JWT tokens, and access control
is enforced on both frontend and backend.

--------------------------------------------------
USER ROLES
--------------------------------------------------
1. Admin
   - Can view all tasks
   - Can assign tasks to users
   - Can update any task they created
   - Can delete tasks
   - Can view any task by ID

2. User
   - Can log in
   - Can view tasks assigned to them
   - Can view task details if assigned
   - Cannot delete tasks
   - Cannot assign tasks to others (unless allowed)

--------------------------------------------------
AUTHENTICATION FLOW
--------------------------------------------------
1. User logs in using username and password.
2. Backend validates credentials.
3. Backend generates JWT token with payload:
   {
     "sub": user.userId,
     "user_role": user.user_role,
     "exp": expiration_time
   }
4. Token is returned to frontend.
5. Frontend stores token in localStorage.
6. All protected API calls send token via Authorization header:
   Authorization: Bearer <token>

--------------------------------------------------
JWT & DEPENDENCIES
--------------------------------------------------
- JWT is decoded in backend using jose.jwt
- `get_current_user` dependency:
  - Extracts token from Authorization header
  - Decodes token
  - Reads userId and user_role
  - Fetches user from database
  - Rejects request if token is invalid or expired

--------------------------------------------------
TASK MANAGEMENT FEATURES
--------------------------------------------------

TASK CREATION
-------------
- Endpoint: POST /tasks/create
- Only logged-in users allowed
- assignedby is automatically taken from logged-in user
- assignedto is selected from existing users
- dueDate format: YYYY:MM:DD

TASK FETCHING
-------------
- Endpoint: GET /tasks
- Admin:
  - Can see all tasks
- User:
  - Can see tasks where:
    - assignedto == logged-in user
    OR
    - assignedby == logged-in user

TASK VIEW BY ID
---------------
- Endpoint: GET /tasks/task/{taskId}
- Admin:
  - Can view any task
- User:
  - Can view task only if assigned to them or created by them

TASK UPDATE
-----------
- Endpoint: PUT /tasks/task/updateAssignedby/{taskId}
- Only task creator (assignedby) can update task
- Updates:
  - name
  - description
  - assignedto
  - dueDate
  - status

TASK DELETE
-----------
- Endpoint: DELETE /tasks/task/{taskId}
- Only admin can delete tasks

--------------------------------------------------
FRONTEND (DASHBOARD)
--------------------------------------------------
- Login protected using token check
- Dashboard UI:
  - Task form on left (Add / Update Task)
  - Task table on right
- Features:
  - Add Task
  - Update Task
  - Delete Task
  - View Task (modal)
  - Clear form button
  - Logout from profile menu

FORM BEHAVIOR
-------------
- Assign Task button (default mode)
- Update Task button (edit mode)
- Clear button resets all fields
- Edit mode updates existing task instead of creating new one

--------------------------------------------------
DATE FORMATTING
--------------------------------------------------
- Backend stores dates as datetime
- Frontend displays:
  - Created At → locale string
  - Deadline → locale date (DD/MM/YYYY or equivalent)

--------------------------------------------------
SECURITY
--------------------------------------------------
- All task routes are protected
- Unauthorized access returns 401 / 403
- Role-based access enforced in backend
- Frontend routes protected using token presence

--------------------------------------------------
DATABASE
--------------------------------------------------
- MySQL database
- Tables:
  - users
  - tasks
  - logged (for active sessions)
- Relationships:
  - User → Tasks (assignedby, assignedto)

--------------------------------------------------
KNOWN LIMITATIONS / NOTES
--------------------------------------------------
- UI styling depends on Dashboard.css
- Admin-only dashboard was restored as primary view
- JWT role decoding is optional on frontend (backend enforces security)
- API paths must exactly match frontend requests

--------------------------------------------------
HOW TO RUN
--------------------------------------------------
Backend:
1. Activate virtual environment
2. Run:
   uvicorn task_management_system.main:app --reload

Frontend:
1. npm install
2. npm start

--------------------------------------------------
END
--------------------------------------------------
