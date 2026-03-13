import React, { useState, useEffect } from 'react';
import { etiquetaService } from '../services/etiquetaService';
import './EtiquetaList.css';

const EtiquetaList = () => {
  const [etiquetas, setEtiquetas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [nuevaEtiqueta, setNuevaEtiqueta] = useState('');

  useEffect(() => {
    cargarEtiquetas();
  }, []);

  const cargarEtiquetas = async () => {
    try {
      setLoading(true);
      const response = await etiquetaService.getAll();
      setEtiquetas(response.data);
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
            <span className="etiqueta-nombre">{etiqueta.nombre}</span>
            <span className="etiqueta-fecha">
              Creada: {new Date(etiqueta.created_at).toLocaleDateString()}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EtiquetaList;