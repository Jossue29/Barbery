document.addEventListener('DOMContentLoaded', function(){
  const buscarBtn = document.getElementById('buscar');
  const telefonoInput = document.getElementById('telefono');
  const clienteInfo = document.getElementById('cliente_info');
  let cliente = null;
  let items = [];

  buscarBtn.addEventListener('click', async ()=>{
    const t = telefonoInput.value.trim();
    if(!t) return;
    const res = await fetch(`/clientes/api/search/?telefono=${encodeURIComponent(t)}`);
    const j = await res.json();
    if(j.ok){
      cliente = j.cliente;
      clienteInfo.innerText = `${cliente.nombre} - ${cliente.telefono}`;
    } else {
      cliente = null;
      clienteInfo.innerText = 'No existe. Crear nuevo.';
    }
  });

  document.getElementById('crear_cliente').addEventListener('click', async ()=>{
    const nombre = document.getElementById('cli_nombre').value;
    const tel = document.getElementById('cli_telefono').value;
    const fd = new FormData();
    fd.append('nombre', nombre);
    fd.append('telefono', tel);
    const res = await fetch('/clientes/api/create/', {method:'POST', body:fd});
    const j = await res.json();
    if(j.ok){
      cliente = j.cliente;
      clienteInfo.innerText = `${cliente.nombre} - ${cliente.telefono}`;
      var myModal = bootstrap.Modal.getInstance(document.getElementById('modalCliente'))
      myModal.hide()
    }
  });

  const tbody = document.querySelector('#detalle tbody');
  function renderItems(){
    tbody.innerHTML = '';
    let total = 0;
    items.forEach((it, idx)=>{
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${it.nombre}</td><td>${it.precio}</td><td>${it.cantidad}</td><td>${(it.precio*it.cantidad).toFixed(2)}</td><td><button data-idx="${idx}" class="btn btn-sm btn-danger del">x</button></td>`
      tbody.appendChild(tr);
      total += it.precio*it.cantidad;
    });
    document.getElementById('total').innerText = total.toFixed(2);
    document.querySelectorAll('.del').forEach(b=>b.addEventListener('click', (e)=>{
      const i = e.target.dataset.idx; items.splice(i,1); renderItems();
    }));
  }

  document.getElementById('add_item').addEventListener('click', ()=>{
    const sel = document.getElementById('select_corte');
    const id = sel.value; const nombre = sel.options[sel.selectedIndex].text; const precio = parseFloat(sel.options[sel.selectedIndex].dataset.precio);
    items.push({corte_id:id, nombre:nombre, precio:precio, cantidad:1});
    renderItems();
  });

  document.getElementById('generar').addEventListener('click', async ()=>{
    if(!cliente){ alert('Seleccione o cree cliente'); return; }
    if(items.length===0){ alert('Agregue al menos un corte'); return; }
    const payload = { cliente_id: cliente.id, barbero_id: document.getElementById('barbero').value, items: items.map(i=>({corte_id:i.corte_id, cantidad:i.cantidad})) };
    const res = await fetch('/facturacion/api/create/', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
    const j = await res.json();
    if(j.ok){
      window.location.href = `/facturacion/ticket/${j.factura_id}/`;
    }
  });

});
