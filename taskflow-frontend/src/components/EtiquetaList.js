import React, { useState, useEffect } from 'react';
import { etiquetaService } from '../services/etiquetaService';
import './EtiquetaList.css';

const EtiquetaList = () => {
  const [etiquetas, setEtiquetas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [nuevaEtiqueta, setNuevaEtiqueta] = useState('');

  // Estado para edición
  const [editandoId, setEditandoId] = useState(null);
  const [nombreEditado, setNombreEditado] = useState('');

  useEffect(() => {
    cargarEtiquetas();
  }, []);

  const cargarEtiquetas = async () => {
    try {
      setLoading(true);
      const response = await etiquetaService.getAll();

      // Fix: manejar cualquier formato de respuesta
      const etiquetasArray =
        Array.isArray(response) ? response :
        response.items || response.data || [];

      setEtiquetas(etiquetasArray);
      setError('');
    } catch (err) {
      setError('Error al cargar las etiquetas');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!nuevaEtiqueta.trim()) return;

    try {
      await etiquetaService.create(nuevaEtiqueta);
      setNuevaEtiqueta('');
      setShowForm(false);
      cargarEtiquetas();
    } catch (err) {
      setError('Error al crear la etiqueta');
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar esta etiqueta?')) {
      try {
        await etiquetaService.delete(id);
        cargarEtiquetas();
      } catch (err) {
        setError('Error al eliminar la etiqueta');
        console.error(err);
      }
    }
  };

  const handleEditarClick = (etiqueta) => {
    setEditandoId(etiqueta.id);
    setNombreEditado(etiqueta.nombre);
  };

  const handleCancelarEdicion = () => {
    setEditandoId(null);
    setNombreEditado('');
  };

  const handleGuardarEdicion = async (id) => {
    if (!nombreEditado.trim()) return;
    try {
      await etiquetaService.update(id, { nombre: nombreEditado });
      setEditandoId(null);
      cargarEtiquetas();
    } catch (err) {
      setError('Error al actualizar la etiqueta');
      console.error(err);
    }
  };

  if (loading) return <div className="loading">Cargando...</div>;

  return (
    <div className="etiqueta-list-container">
      <div className="header">
        <h1>Etiquetas</h1>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Nueva Etiqueta'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {showForm && (
        <form onSubmit={handleSubmit} className="etiqueta-form">
          <input
            type="text"
            placeholder="Nombre de la etiqueta"
            value={nuevaEtiqueta}
            onChange={(e) => setNuevaEtiqueta(e.target.value)}
            required
          />
          <button type="submit" className="btn-success">Crear</button>
        </form>
      )}

      <div className="etiquetas-grid">
        {etiquetas.map(etiqueta => (
          <div key={etiqueta.id} className="etiqueta-card">

            {editandoId === etiqueta.id ? (
              // Modo edición
              <div className="etiqueta-edit-form">
                <input
                  type="text"
                  value={nombreEditado}
                  onChange={(e) => setNombreEditado(e.target.value)}
                  placeholder="Nombre de la etiqueta"
                />
                <div className="edit-buttons">
                  <button
                    className="btn-success"
                    onClick={() => handleGuardarEdicion(etiqueta.id)}
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
              // Modo vista normal
              <>
                <div className="etiqueta-info">
                  <span className="etiqueta-nombre">{etiqueta.nombre}</span>
                  <span className="etiqueta-fecha">
                    Creada: {new Date(etiqueta.created_at).toLocaleDateString()}
                  </span>
                </div>
                <div className="etiqueta-actions">
                  <button
                    className="btn-edit"
                    onClick={() => handleEditarClick(etiqueta)}
                  >
                    ✏️
                  </button>
                  <button
                    className="btn-delete"
                    onClick={() => handleDelete(etiqueta.id)}
                  >
                    ×
                  </button>
                </div>
              </>
            )}

          </div>
        ))}

        {etiquetas.length === 0 && (
          <p className="no-etiquetas">No hay etiquetas aún. ¡Crea una!</p>
        )}
      </div>
    </div>
  );
};

export default EtiquetaList;