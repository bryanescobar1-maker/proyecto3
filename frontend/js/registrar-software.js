document.addEventListener("DOMContentLoaded",()=>{
 const button=document.getElementById("guardarSoftware"); if(!button)return;
 button.addEventListener("click",async()=>{
  const nombre=document.getElementById("nombreSoftware").value.trim();
  const plan=document.getElementById("tipoPlan").value.trim();
  const raw=document.getElementById("costoSoftware").value.replace(/[$, ]/g,"");
  const costo=Number(raw);
  const periodicidad=document.getElementById("periodicidad").value;
  const proximoPago=document.getElementById("proximoPago").value;
  if(!nombre||!plan||!raw||!proximoPago||!Number.isFinite(costo)||costo<0||!Number.isInteger(Number(document.getElementById("licenciasTotales")?.value||0))||Number(document.getElementById("licenciasTotales")?.value||0)<0){alert("Completa los campos con datos válidos");return;}
  const data={providerId:crypto.randomUUID(),nombre,plan,costoMensual:costo,periodicidad,proximoPago,licenciasTotales:Number(document.getElementById("licenciasTotales")?.value||0),licenciasAsignadas:0,estado:"Registrado"};
  try{button.disabled=true;await LicentraAPI.crear("providers",data);alert("Software registrado correctamente");location.href="proveedores.html";}catch(e){alert("No se pudo registrar: "+e.message);}finally{button.disabled=false;}
 });
});
