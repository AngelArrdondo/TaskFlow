import api from './api';

export const tareaService = {
  // Obtener todas las tareas (con filtros)
  getAll: async (completada = null, page = 1, limit = 10) => {
    let url = `/tareas/?page=${page}&limit=${limit}`;
    if (completada !== null) {
      url += `&completada=${completada}`;
    }
    const response = await api.get(url);
    return response.data;
  },

  // Obtener una tarea por ID
  getById: async (id) => {
    const response = await api.get(`/tareas/${id}`);
    return response.data;
  },

  // Crear nueva tarea
  create: async (tarea) => {
    const response = await api.post('/tareas/', tarea);
    return response.data;
  },

  // Actualizar tarea
  update: async (id, tarea) => {
    const response = await api.put(`/tareas/${id}`, tarea);
    return response.data;
  },

  // Marcar como completada
  marcarCompletada: async (id) => {
    const response = await api.patch(`/tareas/${id}/completar`);
    return response.data;
  },

  // Eliminar tarea
  delete: async (id) => {
    await api.delete(`/tareas/${id}`);
    return true;
  },

  // Asignar etiqueta
  asignarEtiqueta: async (tareaId, etiquetaId) => {
    const response = await api.post(`/tareas/${tareaId}/etiquetas`, {
      etiqueta_id: etiquetaId
    });
    return response.data;
  }
};