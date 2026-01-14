// Cliente
const form = document.getElementById('reservaForm');
if(form){
form.addEventListener('submit', async (e)=>{
e.preventDefault();
const data = {
nombre: document.getElementById('nombre').value,
telefono: document.getElementById('telefono').value,
fecha: document.getElementById('fecha').value,
hora: document.getElementById('hora').value,
num_personas: document.getElementById('personas').value
};
const res = await fetch('/api/reserva',{
method:'POST',
headers:{'Content-Type':'application/json'},
body: JSON.stringify(data)
});
const result = await res.json();
const div = document.getElementById('resultado');
if(result.status=='ok'){
div.innerHTML=`Reserva confirmada en mesa ${result.mesa} hasta ${result.hora_fin}`;
}else{
div.innerHTML=`Error: ${result.message}`;
}
});
}

// Admin
async function cargarReservas(){
const res = await fetch('/api/reservas');
const data = await res.json();
const tabla = document.getElementById('tablaReservas');

// Limpiar tabla antes de recargar
while(tabla.rows.length > 1){ // deja la cabecera
    tabla.deleteRow(1);
}

data.forEach(r=>{
const fila = tabla.insertRow();
fila.insertCell(0).innerText = r.nombre;
fila.insertCell(1).innerText = r.telefono;
fila.insertCell(2).innerText = r.fecha;
fila.insertCell(3).innerText = r.hora_inicio;
fila.insertCell(4).innerText = r.hora_fin;
fila.insertCell(5).innerText = r.num_personas;
fila.insertCell(6).innerText = r.mesa;

// Botón borrar
const celdaBorrar = fila.insertCell(7);
const btn = document.createElement('button');
btn.innerText = 'Borrar';
btn.onclick = async ()=>{
if(confirm(`¿Seguro que quieres borrar la reserva de ${r.nombre}?`)){
await fetch(`/api/reserva/${r.id}`, { method: 'DELETE' });
fila.remove(); // eliminar fila de la tabla
}
};
celdaBorrar.appendChild(btn);
});
}

// Cargar reservas al iniciar admin
if(document.getElementById('tablaReservas')){
cargarReservas();

// (Opcional) refrescar cada 10 segundos automáticamente
setInterval(cargarReservas, 10000);
}

// Service Worker (para PWA)
if('serviceWorker' in navigator){
navigator.serviceWorker.register('/static/sw.js')
.then(()=>console.log('Service Worker registrado'));
}
