(function () {
  const entityKey = '[ENTITY_KEY]';
  const hiddenKey = entityKey + '.hiddenCols';
  const table = document.getElementById(entityKey + '-table');
  const selectAll = document.getElementById(entityKey + '-select-all');
  const columnToggles = document.querySelectorAll('#' + entityKey + '-columns input[type="checkbox"]');
  const offcanvasEl = document.getElementById('offcanvasDetail');
  const offcanvas = offcanvasEl ? new bootstrap.Offcanvas(offcanvasEl) : null;
  const liveRegion = document.getElementById(entityKey + '-filters-status');

  // Atajos de teclado
  document.addEventListener('keydown', function (e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === 'n' || e.key === 'N') {
      window.location.href = '[CREATE_ROUTE]';
    }
    if (e.key === 'f' || e.key === 'F') {
      const search = document.querySelector('#' + entityKey + '-filters input[name="search"]');
      if (search) {
        search.focus();
      }
    }
    if (e.key === '?') {
      const modal = document.getElementById('shortcutsModal');
      if (modal) {
        new bootstrap.Modal(modal).show();
      }
    }
  });

if (table) {
  // Selección masiva
  function updateSelection() {
    const checked = table.querySelectorAll('tbody input[type="checkbox"]:checked');
    const actions = document.querySelectorAll('[data-bulk-action]');
    actions.forEach(btn => btn.disabled = checked.length === 0);
  }
  if (selectAll) {
    selectAll.addEventListener('change', function () {
      const boxes = table.querySelectorAll('tbody input[type="checkbox"]');
      boxes.forEach(cb => cb.checked = selectAll.checked);
      updateSelection();
    });
  }
  table.addEventListener('change', function (e) {
    if (e.target.matches('tbody input[type="checkbox"]')) {
      updateSelection();
    }
  });

  // Column toggles
  const hiddenCols = JSON.parse(localStorage.getItem(hiddenKey) || '[]');
  hiddenCols.forEach(name => {
    const checkbox = document.querySelector('#' + entityKey + '-columns input[data-column="' + name + '"]');
    if (checkbox) {
      checkbox.checked = false;
      toggleColumn(name, false);
    }
  });

  function toggleColumn(name, visible) {
    const cells = table.querySelectorAll('[data-col="' + name + '"]');
    cells.forEach(c => c.classList.toggle('d-none', !visible));
    announce('Columna ' + name + (visible ? ' visible' : ' oculta'));
  }

  columnToggles.forEach(cb => {
    cb.addEventListener('change', function () {
      toggleColumn(cb.dataset.column, cb.checked);
      let stored = JSON.parse(localStorage.getItem(hiddenKey) || '[]');
      if (!cb.checked) {
        if (!stored.includes(cb.dataset.column)) stored.push(cb.dataset.column);
      } else {
        stored = stored.filter(i => i !== cb.dataset.column);
      }
      localStorage.setItem(hiddenKey, JSON.stringify(stored));
    });
  });

  // Offcanvas detalle
  document.querySelectorAll('.detail-trigger').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const row = e.target.closest('tr');
      const id = row.dataset.id;
      const nameCell = row.querySelector('.' + entityKey + '-name');
      if (!offcanvas) return;
      // TODO: endpoint de detalle
      fetch('/[ENTITY_NAME]/' + id + '/detail/')
        .then(r => r.ok ? r.json() : Promise.reject())
        .then(data => populateDetail(data))
        .catch(() => {
          populateDetail({
            name: nameCell ? nameCell.textContent.trim() : '',
          });
        });
      offcanvas.show();
    });
  });
}

  function populateDetail(data) {
    const content = document.getElementById('offcanvasContent');
    content.innerHTML = '<strong>' + (data.name || '') + '</strong>';
    document.getElementById('offcanvasEdit').href = '[EDIT_ROUTE(:id)]'.replace(':id', data.id || '');
    document.getElementById('offcanvasDelete').href = '[DELETE_ROUTE(':id)]'.replace(':id', data.id || '');
  }

  function announce(msg) {
    if (liveRegion) {
      liveRegion.textContent = msg;
    }
  }
})();
