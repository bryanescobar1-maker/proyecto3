// Cambia esta URL por la de API Gateway cuando publiques el backend.
const API_URL = "http://127.0.0.1:5000";
async function requestAPI(path, options = {}) {
  const response = await fetch(API_URL + path, { ...options, headers: { "Content-Type": "application/json", ...options.headers } });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Error al consultar el servidor");
  return data;
}
const LicentraAPI = {
  listar: entity => requestAPI(`/api/${entity}`),
  obtener: (entity, id) => requestAPI(`/api/${entity}/${encodeURIComponent(id)}`),
  crear: (entity, data) => requestAPI(`/api/${entity}`, {method:"POST", body:JSON.stringify(data)}),
  actualizar: (entity, id, data) => requestAPI(`/api/${entity}/${encodeURIComponent(id)}`, {method:"PUT", body:JSON.stringify(data)}),
  asignar: data => requestAPI("/api/assignments", {method:"POST",body:JSON.stringify(data)}),
  liberar: id => requestAPI(`/api/assignments/${encodeURIComponent(id)}`, {method:"DELETE"}),
  eliminar: (entity, id) => requestAPI(`/api/${entity}/${encodeURIComponent(id)}`, {method:"DELETE"})
};
