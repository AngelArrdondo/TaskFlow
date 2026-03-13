import api from './api';

export const etiquetaService = {
  // Obtener todas las etiquetas
  getAll: async () => {
    const response = await api.get('/etiquetas/');
    return response.data;
  },

  // Crear nueva etiqueta
  create: async (nombre) => {
    const response = await api.post('/etiquetas/', { nombre });
    return response.data;
  }
};