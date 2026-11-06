let providers = [];
const money = value => "$" + Number(value || 0).toLocaleString("en-US", {maximumFractionDigits:2});
function renderProviders(items) {
 const tbody = document.querySelector(".employees-table tbody"); if (!tbody) return;
 tbody.replaceChildren();
 if (!items.length) {const tr=tbody.insertRow(); const td=tr.insertCell(); td.colSpan=7; td.textContent="No hay proveedores registrados en DynamoDB"; td.style.padding="25px"; return;}
 for (const p of items) {
   const tr=tbody.insertRow();
   const info=tr.insertCell(); const wrap=document.createElement("div"); wrap.className="employee-info";
   const avatar=document.createElement("div"); avatar.className="employee-avatar"; avatar.style.cssText="background:#4f46e5;color:white"; avatar.textContent=(p.nombre||"?").slice(0,2).toUpperCase();
   const details=document.createElement("div"); const name=document.createElement("div"); name.className="employee-name"; name.textContent=p.nombre||"Sin nombre"; const desc=document.createElement("div"); desc.className="employee-email"; desc.textContent=p.descripcion||"Servicio SaaS"; details.append(name,desc); wrap.append(avatar,details); info.append(wrap);
   [p.plan||"-", money(p.costoMensual), p.proximoPago||"-", `${p.licenciasAsignadas||0} de ${p.licenciasTotales||0}`, p.estado||"Registrado"].forEach(value=>tr.insertCell().textContent=value);
   const actions=tr.insertCell(); actions.style.textAlign="right";
   const edit=document.createElement("button"); edit.type="button"; edit.textContent="Editar"; edit.className="filter-btn"; edit.style.marginRight="6px"; edit.onclick=()=>editProvider(p);
   const del=document.createElement("button"); del.type="button"; del.textContent="Eliminar"; del.className="filter-btn"; del.onclick=()=>deleteProvider(p.providerId);
   actions.append(edit,del);
 }
}
async function loadProviders(){try{providers=await LicentraAPI.listar("providers"); filterProviders(); updateProviderMetrics();}catch(e){console.error(e); alert("No se pudieron cargar los proveedores: "+e.message);}}
function filterProviders(){const input=document.querySelector('input[placeholder="Buscar software o proveedor..."]'); const q=(input?.value||"").toLowerCase(); renderProviders(providers.filter(p=>(p.nombre||"").toLowerCase().includes(q)));}
function updateProviderMetrics(){const numbers=document.querySelectorAll(".metrics-row strong"); if(numbers.length>=3){numbers[0].textContent=String(providers.length).padStart(2,"0"); numbers[1].textContent=money(providers.reduce((a,p)=>a+Number(p.costoMensual||0),0)); const soon=providers.filter(p=>{if(!p.proximoPago)return false;const d=(new Date(p.proximoPago+"T00:00:00")-new Date())/86400000;return d>=-1&&d<=10;});numbers[2].textContent=String(soon.length).padStart(2,"0");}}
async function editProvider(p){const plan=prompt("Nuevo plan",p.plan||"");if(plan===null)return;const value=prompt("Nuevo costo mensual",p.costoMensual||0);if(value===null)return;const next=prompt("Próxima fecha de pago (AAAA-MM-DD)",p.proximoPago||"");if(next===null)return;const period=prompt("Periodicidad: Mensual o Anual",p.periodicidad||"Mensual");if(period===null)return;const seatsRaw=prompt("Cantidad de licencias contratadas",p.licenciasTotales||0);if(seatsRaw===null)return;const seats=Number(seatsRaw);const cost=Number(value);if(!Number.isInteger(seats)||seats<0){alert("La cantidad de licencias debe ser un entero no negativo");return;}if(!plan.trim()||!Number.isFinite(cost)||cost<0){alert("Datos inválidos");return;}try{await LicentraAPI.actualizar("providers",p.providerId,{plan:plan.trim(),costoMensual:cost,licenciasTotales:seats,proximoPago:next,periodicidad:period});await loadProviders();}catch(e){alert(e.message);}}
async function deleteProvider(id){if(!confirm("¿Eliminar este proveedor?"))return;try{await LicentraAPI.eliminar("providers",id);await loadProviders();}catch(e){alert(e.message);}}
document.addEventListener("DOMContentLoaded",()=>{document.querySelector('.page-header .btn-primary')?.addEventListener("click",()=>location.href="registrar-software.html");document.querySelector('input[placeholder="Buscar software o proveedor..."]')?.addEventListener("input",filterProviders);loadProviders();});
