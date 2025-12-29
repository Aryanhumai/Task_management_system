import { useEffect, useState } from 'react'
import "./css/Dashboard.css"
import { Icon } from "@iconify/react";
import { Link } from "react-router";
import axios from 'axios';
import { CONFIG } from '../../config/CONFIG';
import { getToken } from '../../util/manageToken';
import { toast } from 'react-toastify';
import { useNavigate } from "react-router-dom";
import { clearToken } from "../../util/manageToken";




function Dashboard() {

    const [taskList, setTaskList] = useState([]);
    const [title, setTitle] = useState("");
    const [assignedTo, setAssignedTo] = useState("");
    // const [assignedBy, setAssignedBy] = useState("");
    const [deadline, setDeadline] = useState("");

    const [selectedTask, setSelectedTask] = useState(null);
    const [isViewOpen, setIsViewOpen] = useState(false);
    const [isEditOpen, setIsEditOpen] = useState(false);
    const [showProfileMenu, setShowProfileMenu] = useState(false);
    const [users, setUsers] = useState([]);

    const [isEditMode, setIsEditMode] = useState(false);
    const [editingTaskId, setEditingTaskId] = useState(null);




    async function getTaskList() {
        try {
            let res = await axios.get(CONFIG.BASE_URL + "/tasks/", {
                headers: { Authorization: `Bearer ${getToken()}` }
            })
            // toast.success("task loaded successfully!");
            setTaskList(res?.data)

        } catch (err) {
            toast.error("Task Load Failed!");
            console.log("err- ", err)
        }

    }

    async function handleAddTask() {
        if (isEditMode) return;

        if (!title || !assignedTo || !deadline) {
            toast.error("All fields are required");
            return;
        }

        try {
            await axios.post(
                CONFIG.BASE_URL + "/tasks/create",
                {
                    name: title,                 // REQUIRED by backend
                    description: title,          // optional but ok
                    // assignedby: assignedBy,
                    assignedto: assignedTo,
                    dueDate: deadline.replaceAll("-", ":")
                },
                {
                    headers: {
                        Authorization: `Bearer ${getToken()}`
                    }
                }
            );

            toast.success("Task added successfully");

            // clear inputs
            setTitle("");
            setAssignedTo("");
            // setAssignedBy("");
            setDeadline("");

            // refresh table
            getTaskList();

        } catch (err) {
            console.log("ADD TASK ERROR 👉", err.response?.data || err.message);
            toast.error(err.response?.data?.message || "Failed to add task");
        }

    }

    async function handleDeleteTask(taskId) {
        if (!window.confirm("Are you sure you want to delete this task?")) return;

        try {
            await axios.delete(
                CONFIG.BASE_URL + `/tasks/task/${taskId}`,
                {
                    headers: {
                        Authorization: `Bearer ${getToken()}`
                    }
                }
            );

            toast.success("Task deleted");
            setIsEditOpen(false);       // 🔥 ADD
            setSelectedTask(null);
            getTaskList();

        } catch (err) {
            toast.error("Failed to delete task");
            console.log(err);
        }
    }

    function handleViewTask(task) {
        setSelectedTask(task);
        setIsViewOpen(true);
    }

    function handleEditTask(task) {
        setIsEditMode(true);
        setEditingTaskId(task.taskId);
        setIsViewOpen(false);
        setSelectedTask(task);
        setTitle(task.name);
        // setAssignedBy(task.assignedby);
        setAssignedTo(task.assignedto);
        setDeadline(String(task.dueDate).slice(0, 10));
        setIsEditOpen(true);
    }

    async function handleUpdateTask() {
        console.log("🔥 UPDATE BUTTON CLICKED", selectedTask);

        if (!selectedTask?.taskId) {
            toast.error("No task selected for update");
            return;
        }
        try {
            await axios.put(
                `${CONFIG.BASE_URL}/tasks/task/updateAssignedby/${selectedTask.taskId}`,
                {
                    name: title,
                    // assignedby: assignedBy,
                    assignedto: assignedTo,
                    dueDate: deadline.replaceAll("-", ":")
                },
                {
                    headers: {
                        Authorization: `Bearer ${getToken()}`
                    }
                }
            );

            toast.success("Task updated successfully");
            setIsEditOpen(false);
            setIsEditMode(false);  
            setSelectedTask(null);
            setEditingTaskId(null);
            getTaskList();

        } catch (err) {
            toast.error("Failed to update task");
            console.log(err.response?.data || err);
        }
    }

    const navigate = useNavigate();

    function handleLogout() {
        if (!window.confirm("Are you sure you want to logout?")) return;
        clearToken();              // remove token
        toast.success("Logged out successfully");
        navigate("/login");        // redirect to login
    }

    function clearFields() {
        setTitle("");
        setAssignedTo("");
        // setAssignedBy("");
        setDeadline("");
        setSelectedTask(null);
        setIsEditOpen(false);
    }

    async function getUsers() {
        try {
            const res = await axios.get(
                `${CONFIG.BASE_URL}/users/users`,
                {
                    headers: {
                        Authorization: `Bearer ${getToken()}`
                    }
                }
            );
            setUsers(res.data);
        } catch (err) {
            toast.error("Failed to load users");
            console.log(err);
        }
    }








    useEffect(() => {
        getTaskList();
        getUsers();
    }, [])

    return (


        <header>
            <nav>
                <div className="left">Task management system</div>

                <div className="menu-toggle" id="menu-toggle">
                    <div className="bar"></div>
                    <div className="bar"></div>
                    <div className="bar"></div>
                </div>

                <div className="right">
                    <ul id="nav-list">
                        <li>
                            <Link to="/Dashboard">
                                Dashboard
                            </Link>
                        </li>
                        <li>
                            <Link to="/about">
                                About
                            </Link>
                        </li>
                        <li>
                            <Link to="#">
                                Tasks
                            </Link>
                        </li>
                        <li
                            className="profile-menu"
                            onClick={() => setShowProfileMenu(prev => !prev)}
                        >
                            Profile ▾

                            {showProfileMenu && (
                                <ul className="profile-dropdown">
                                    <li onClick={handleLogout}>Logout</li>
                                </ul>
                            )}
                        </li>


                    </ul>
                </div>
            </nav>

            <section className="main">

                <aside className="card">
                    <h3>{isEditOpen ? "Update Task" : "Add Task"} :-</h3>
                    <hr />
                    <br />
                    <div className="field">
                        <label>Task Title:</label>
                        <input
                            type="text"
                            placeholder="Enter title"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                        />
                    </div>
                    <div className="field">
                        <label>Assigned to:</label>
                        <select
                            value={assignedTo}
                            onChange={(e) => setAssignedTo(e.target.value)}
                        >
                            <option value="">Select user</option>
                            {users.map((user) => (
                                <option key={user.userId} value={user.userId}>
                                    {user.name} ({user.userId})
                                </option>
                            ))}
                        </select>


                    </div>
                    {/* <div className="field">
                        <label>Assigned by:</label>
                        <input
                            type="text"
                            placeholder="Eid"
                            value={assignedBy}
                            onChange={(e) => setAssignedBy(e.target.value)}
                        />

                    </div> */}
                    <div className="field">
                        <label>Deadline:</label>
                        <input
                            type="date"
                            className="small"
                            value={deadline}
                            onChange={(e) => setDeadline(e.target.value)}
                        />

                    </div>
                    {/* <button className="btn" onClick={handleAddTask}>
                        Assign Task
                    </button> */}

                    <div style={{ display: "flex", gap: "10px" }}>
                        {!isEditOpen ? (
                            <button className="btn" onClick={handleAddTask}>
                                Assign Task
                            </button>
                        ) : (
                            <button
                                type="button"
                                className="btn"
                                onClick={handleUpdateTask}
                            >
                                Update Task
                            </button>
                        )}

                        <button
                            type="button"
                            className="btn secondary"
                            onClick={clearFields}
                        >
                            Clear
                        </button>
                    </div>



                    {/* <button
                        type="button"
                        className="btn"
                        onClick={handleUpdateTask}
                        disabled={!isEditOpen}
                    >
                        Update Task
                    </button> */}



                </aside>

                <table className="task-table" border="1">
                    <thead>
                        <tr>
                            <th>S.no</th>
                            <th>Title</th>
                            <th>Date</th>
                            <th>Assigned By</th>
                            <th>Assigned To</th>
                            <th>Created At</th>
                            <th>Deadline</th>
                            <th>Action</th>
                        </tr>
                    </thead>

                    <tbody>
                        {taskList?.map((item, index) => {
                            console.log(item)
                            return (
                                <tr key={index}>
                                    <td>{index + 1}</td>
                                    <td>{item?.description}</td>
                                    <td>{item?.createdAt}</td>
                                    <td>{item?.assignedby}</td>
                                    <td>{item?.assignedto}</td>
                                    <td>
                                        {new Date(item.createdAt).toLocaleString()}
                                    </td>

                                    <td>
                                        {new Date(item.dueDate).toLocaleDateString()}
                                    </td>

                                    <td className="action-icons">
                                        <Icon
                                            icon="hugeicons:view"
                                            onClick={() => handleViewTask(item)}
                                            style={{ cursor: "pointer" }}
                                        />

                                        <Icon
                                            icon="material-symbols:edit"
                                            onClick={() => handleEditTask(item)}
                                            style={{ cursor: "pointer" }}
                                        />

                                        <Icon
                                            icon="material-symbols:delete"
                                            onClick={() => handleDeleteTask(item.taskId)}
                                            style={{ cursor: "pointer" }}
                                        />

                                    </td>
                                </tr>
                            )
                        })}




                    </tbody>
                </table>

            </section>

            <footer className="site-footer">
                <div className="footer-top">
                    <div className="brand">
                        <h3>Aryan's Task Management</h3>
                    </div>

                    <div className="footer-links" aria-label="Footer navigation">
                        <a href="#">Home</a>
                        <a href="#">About</a>
                        <a href="#">Services</a>
                        <a href="#">Contact</a>
                    </div>

                    <div className="footer-social" aria-label="Social links">
                        <a href="#" className="social-item">Instagram</a>
                        <a href="#" className="social-item">LinkedIn</a>
                        <a href="#" className="social-item">GitHub</a>
                        <a href="mailto:youremail@example.com" className="social-item">Gmail</a>
                    </div>
                </div>

                <div className="footer-bottom">
                    <p>© <span id="year"></span> xyz. All rights reserved.</p>
                    <p>Designed by <strong>Aryan Bhatia</strong></p>
                </div>
            </footer>
            {isViewOpen && selectedTask && (
                <div className="modal-overlay">
                    <div className="modal">
                        <h3>View Task</h3>
                        <p><b>Title:</b> {selectedTask.name}</p>
                        <p><b>Description:</b> {selectedTask.description}</p>
                        <p><b>Assigned By:</b> {selectedTask.assignedby}</p>
                        <p><b>Assigned To:</b> {selectedTask.assignedto}</p>

                        <p>
                            <b>Created At:</b>{" "}
                            {new Date(selectedTask.createdAt).toLocaleString()}
                        </p>

                        <p>
                            <b>Deadline:</b>{" "}
                            {new Date(selectedTask.dueDate).toLocaleDateString()}
                        </p>


                        <button onClick={() => setIsViewOpen(false)}>Close</button>
                    </div>
                </div>
            )}

        </header>

    )
}

export default Dashboard