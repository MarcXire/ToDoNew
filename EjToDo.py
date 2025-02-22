import streamlit as st
import os
import json
import datetime

#$env:Path += ";C:\Users\User\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts"
#streamlit run EjToDo.py --server.address 0.0.0.0 --server.port 8080

#http://192.168.1.143:8501



# Datos de usuarios y contraseñas
users = {
    "marc": "mt",
    "inma": "it",
    "luis": "lt"
}

# Inicializar session_state si no existen
if "user" not in st.session_state:
    st.session_state["user"] = None
if "tk_file" not in st.session_state:
    st.session_state["tk_file"] = None
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []
if "fecha_activada" not in st.session_state:
    st.session_state["fecha_activada"] = False  # Indica si se activó la fecha
if "fecha_seleccionada" not in st.session_state:
    st.session_state["fecha_seleccionada"] = datetime.date.today()  # Fecha por defecto

# Función para cargar tareas
def load_tasks():
    if os.path.exists(st.session_state["tk_file"]):
        try:
            with open(st.session_state["tk_file"], "r") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []
    return []

# Función para guardar tareas
def save_tasks():
    with open(st.session_state["tk_file"], "w") as file:
        json.dump(st.session_state["tasks"], file, indent=4)

# Función para ordenar tareas por fecha
def sort_tasks():
    def task_key(task):
        if "date" in task:
            return datetime.datetime.strptime(task["date"], "%Y-%m-%d").date()
        return datetime.date.max
    st.session_state["tasks"].sort(key=task_key)

# UI de Streamlit
st.title("Lista de :red[Tareas]")

# Si el usuario no está autenticado, mostrar login
if st.session_state["user"] is None:
    with st.form("acount"):
        acc = st.text_input("Usuario")
        cc = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar sesión")

        if submitted:
            if acc in users and users[acc] == cc:
                st.session_state["user"] = acc
                st.session_state["tk_file"] = f"{acc}_tasks.json"
                st.session_state["tasks"] = load_tasks()
                sort_tasks()
                st.success(f"Inicio de sesión exitoso para {acc}")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

# Si el usuario ya está autenticado
if st.session_state["user"]:
    st.write(f"👤 Usuario autenticado: **{st.session_state['user']}**")

    # Formulario para agregar tareas
    tk_name = st.text_input("Task codename")
    tk_desc = st.text_input("Task description")

    # Checkbox para ver si la tarea tiene fecha
    fecha = st.checkbox("La tarea tiene fecha", value=st.session_state["fecha_activada"])

    # Si el checkbox está marcado, se activa el calendario
    if fecha:
        st.session_state["fecha_activada"] = True
        st.session_state["fecha_seleccionada"] = st.date_input("Fecha de la tarea:", value=st.session_state["fecha_seleccionada"])
    else:
        st.session_state["fecha_activada"] = False

    # Botón para agregar la tarea
    if st.button("Agregar tarea"):
        new_task = {"name": tk_name, "description": tk_desc}
        if st.session_state["fecha_activada"]:
            new_task["date"] = str(st.session_state["fecha_seleccionada"])
        
        st.session_state["tasks"].append(new_task)
        sort_tasks()
        save_tasks()
        st.success(f"Tarea '{tk_name}' guardada con éxito!")
        st.rerun()

    # Mostrar tareas guardadas con opción de eliminar
    st.subheader("📋 Tareas guardadas (Ordenadas por fecha 📅):")
    if st.session_state["tasks"]:
        for i, task in enumerate(st.session_state["tasks"]):
            col1, col2 = st.columns([4, 1])
            with col1:
                task_info = f"**{task['name']}** → {task['description']}"
                if "date" in task:
                    task_info += f" 📅 {task['date']}"
                st.write(task_info)
            with col2:
                if st.button("❌", key=f"delete_{i}"):
                    del st.session_state["tasks"][i]
                    save_tasks()
                    st.rerun()
    else:
        st.write("No hay tareas aún.")

    # Botón para cerrar sesión
    if st.button("Cerrar sesión"):
        st.session_state["user"] = None
        st.session_state["tk_file"] = None
        st.session_state["tasks"] = []
        st.session_state["fecha_activada"] = False
        st.session_state["fecha_seleccionada"] = datetime.date.today()
        st.rerun()
