import React, { useState, useEffect } from 'react';
import { tareaService } from '../services/tareaService';
import { etiquetaService } from '../services/etiquetaService';
import './TareaList.css';

const TareaList = () => {
  const [tareas, setTareas] = useState([]);
  const [etiquetas, setEtiquetas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filtro, setFiltro] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [showForm, setShowForm] = useState(false);

  // Estados para edición
  const [editandoId, setEditandoId] = useState(null);
  const [tareaEditada, setTareaEditada] = useState({
    titulo: '',
    descripcion: '',
    fecha_limite: '',
    completada: false
  });

  const [nuevaTarea, setNuevaTarea] = useState({
    titulo: '',
    descripcion: '',
    fecha_limite: '',
    completada: false
  });

  useEffect(() => {
    cargarTareas();
    cargarEtiquetas();
  }, [filtro, page]);

  const cargarTareas = async () => {
    try {
      setLoading(true);
      const response = await tareaService.getAll(filtro, page);
      console.log("RESPUESTA API TAREAS:", response);
      const tareasArray =
        Array.isArray(response) ? response :
        response.items || response.data || [];
      setTareas(tareasArray);
      setTotalPages(response.meta?.pages || 1);
      setError('');
    } catch (err) {
      setError('Error al cargar las tareas');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const cargarEtiquetas = async () => {
    try {
      const response = await etiquetaService.getAll();
      console.log("RESPUESTA API ETIQUETAS:", response);
      const etiquetasArray =
        Array.isArray(response) ? response :
        response.items || response.data || [];
      setEtiquetas(etiquetasArray);
    } catch (err) {
      console.error('Error al cargar etiquetas:', err);
      setEtiquetas([]);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setNuevaTarea({
      ...nuevaTarea,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await tareaService.create(nuevaTarea);
      setShowForm(false);
      setNuevaTarea({
        titulo: '',
        descripcion: '',
        fecha_limite: '',
        completada: false
      });
      cargarTareas();
    } catch (err) {
      setError('Error al crear la tarea');
      console.error(err);
    }
  };

  const handleToggleCompletada = async (id, completada) => {
    try {
      if (!completada) {
        await tareaService.marcarCompletada(id);
      }
      cargarTareas();
    } catch (err) {
      setError('Error al actualizar la tarea');
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar esta tarea?')) {
      try {
        await tareaService.delete(id);
        cargarTareas();
      } catch (err) {
        setError('Error al eliminar la tarea');
        console.error(err);
      }
    }
  };

  const handleAsignarEtiqueta = async (tareaId, etiquetaId) => {
    if (!etiquetaId) return;
    try {
      await tareaService.asignarEtiqueta(tareaId, etiquetaId);
      cargarTareas();
    } catch (err) {
      setError('Error al asignar etiqueta');
      console.error(err);
    }
  };

  // Funciones de edición
  const handleEditarClick = (tarea) => {
    setEditandoId(tarea.id);
    setTareaEditada({
      titulo: tarea.titulo || '',
      descripcion: tarea.descripcion || '',
      fecha_limite: tarea.fecha_limite || '',
      completada: tarea.completada || false
    });
  };

  const handleCancelarEdicion = () => {
    setEditandoId(null);
    setTareaEditada({
      titulo: '',
      descripcion: '',
      fecha_limite: '',
      completada: false
    });
  };

  const handleGuardarEdicion = async (id) => {
    try {
      await tareaService.update(id, tareaEditada);
      setEditandoId(null);
      cargarTareas();
    } catch (err) {
      setError('Error al actualizar la tarea');
      console.error(err);
    }
  };

  const handleEditInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setTareaEditada({
      ...tareaEditada,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  if (loading && tareas.length === 0) {
    return <div className="loading">Cargando...</div>;
  }

  return (
    <div className="tarea-list-container">

      <div className="header">
        <h1>Mis Tareas</h1>
        <button
          className="btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancelar' : '+ Nueva Tarea'}
        </button>
      </div>

      {error && (
        <div className="error-message">{error}</div>
      )}

      {showForm && (
        <form onSubmit={handleSubmit} className="tarea-form">
          <input
            type="text"
            name="titulo"
            placeholder="Título"
            value={nuevaTarea.titulo}
            onChange={handleInputChange}
            required
          />
          <textarea
            name="descripcion"
            placeholder="Descripción"
            value={nuevaTarea.descripcion}
            onChange={handleInputChange}
          />
          <input
            type="date"
            name="fecha_limite"
            value={nuevaTarea.fecha_limite}
            onChange={handleInputChange}
          />
          <label>
            <input
              type="checkbox"
              name="completada"
              checked={nuevaTarea.completada}
              onChange={handleInputChange}
            />
            Completada
          </label>
          <button type="submit" className="btn-success">
            Crear Tarea
          </button>
        </form>
      )}

      <div className="filtros">
        <button
          className={`btn-filtro ${filtro === null ? 'active' : ''}`}
          onClick={() => setFiltro(null)}
        >
          Todas
        </button>
        <button
          className={`btn-filtro ${filtro === false ? 'active' : ''}`}
          onClick={() => setFiltro(false)}
        >
          Pendientes
        </button>
        <button
          className={`btn-filtro ${filtro === true ? 'active' : ''}`}
          onClick={() => setFiltro(true)}
        >
          Completadas
        </button>
      </div>

      <div className="tareas-grid">
        {tareas.map(tarea => (
          <div
            key={tarea.id}
            className={`tarea-card ${tarea.completada ? 'completada' : ''}`}
          >

            {/* MODO EDICIÓN */}
            {editandoId === tarea.id ? (
              <div className="tarea-edit-form">
                <input
                  type="text"
                  name="titulo"
                  value={tareaEditada.titulo}
                  onChange={handleEditInputChange}
                  placeholder="Título"
                  required
                />
                <textarea
                  name="descripcion"
                  value={tareaEditada.descripcion}
                  onChange={handleEditInputChange}
                  placeholder="Descripción"
                />
                <input
                  type="date"
                  name="fecha_limite"
                  value={tareaEditada.fecha_limite}
                  onChange={handleEditInputChange}
                />
                <label>
                  <input
                    type="checkbox"
                    name="completada"
                    checked={tareaEditada.completada}
                    onChange={handleEditInputChange}
                  />
                  Completada
                </label>
                <div className="edit-buttons">
                  <button
                    className="btn-success"
                    onClick={() => handleGuardarEdicion(tarea.id)}
                  >
                    Guardar
                  </button>
                  <button
                    className="btn-cancel"
                    onClick={handleCancelarEdicion}
                  >
                    Cancelar
                  </button>
                </div>
              </div>

            ) : (
              /* MODO VISTA NORMAL */
              <>
                <div className="tarea-header">
                  <h3>{tarea.titulo}</h3>
                  <div className="tarea-actions">
                    <button
                      className="btn-edit"
                      onClick={() => handleEditarClick(tarea)}
                    >
                      ✏️
                    </button>
                    <button
                      className="btn-toggle"
                      onClick={() => handleToggleCompletada(tarea.id, tarea.completada)}
                    >
                      {tarea.completada ? '✓' : '○'}
                    </button>
                    <button
                      className="btn-delete"
                      onClick={() => handleDelete(tarea.id)}
                    >
                      ×
                    </button>
                  </div>
                </div>

                {tarea.descripcion && (
                  <p className="tarea-descripcion">{tarea.descripcion}</p>
                )}

                {tarea.fecha_limite && (
                  <p className="tarea-fecha">
                    <strong>Límite:</strong>{" "}
                    {new Date(tarea.fecha_limite).toLocaleDateString()}
                  </p>
                )}

                <div className="etiquetas-container">
                  {tarea.etiquetas?.map(etiqueta => (
                    <span key={etiqueta.id} className="etiqueta">
                      {etiqueta.nombre}
                    </span>
                  ))}
                  <select
                    className="select-etiqueta"
                    onChange={(e) =>
                      handleAsignarEtiqueta(tarea.id, parseInt(e.target.value))
                    }
                    value=""
                  >
                    <option value="">+ Asignar etiqueta</option>
                    {etiquetas
                      .filter(e => !tarea.etiquetas?.some(te => te.id === e.id))
                      .map(e => (
                        <option key={e.id} value={e.id}>
                          {e.nombre}
                        </option>
                      ))
                    }
                  </select>
                </div>
              </>
            )}

          </div>
        ))}
      </div>

      {totalPages > 1 && (
        <div className="paginacion">
          <button
            disabled={page === 1}
            onClick={() => setPage(p => p - 1)}
          >
            Anterior
          </button>
          <span>Página {page} de {totalPages}</span>
          <button
            disabled={page === totalPages}
            onClick={() => setPage(p => p + 1)}
          >
            Siguiente
          </button>
        </div>
      )}

    </div>
  );
};

export default TareaList;