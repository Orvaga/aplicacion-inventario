// table-excel.js
// Proporciona comportamiento básico tipo hoja de cálculo:
// - navegar con flechas
// - doble clic o Enter para editar celda
// - ESC para cancelar, Enter para aceptar
// - Ctrl+C / Ctrl+V soporte simple
// - selección de una celda activa

(function(){
    function isEditableCell(td) {
        if (!td) return false;
        // evitamos acciones (botones) si contienen botones
        if (td.querySelector('a, button')) return false;
        return true;
    }

    function makeExcelGrid(table) {
        if (!table) return;
        table.setAttribute('tabindex','0');
        table.classList.add('excel-enabled');

        let active = null;
        let clipboard = '';

        function setActive(td) {
            if (active) active.classList.remove('active-cell');
            active = td;
            if (active) {
                active.classList.add('active-cell');
                active.focus();
            }
        }

        // handle click: set active
        table.addEventListener('click', function(e){
            const td = e.target.closest('td');
            if (!td) return;
            setActive(td);
        });

        // keyboard navigation and editing
        table.addEventListener('keydown', function(e){
            if (!active) return;
            const tr = active.parentElement;
            const row = Array.from(table.tBodies[0].rows).indexOf(tr);
            const col = Array.from(tr.cells).indexOf(active);

            // editar: Enter o F2
            if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey && !e.altKey) {
                e.preventDefault();
                startEdit(active);
                return;
            }
            if (e.key === 'F2') { e.preventDefault(); startEdit(active); return; }

            if (e.key === 'ArrowDown') { e.preventDefault(); moveTo(row+1, col); return; }
            if (e.key === 'ArrowUp') { e.preventDefault(); moveTo(row-1, col); return; }
            if (e.key === 'ArrowLeft') { e.preventDefault(); moveTo(row, col-1); return; }
            if (e.key === 'ArrowRight') { e.preventDefault(); moveTo(row, col+1); return; }

            // copiar
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'c') {
                e.preventDefault();
                if (active) {
                    clipboard = active.textContent.trim();
                    try { navigator.clipboard && navigator.clipboard.writeText(clipboard); } catch (e) {}
                    highlightCopy(active);
                }
                return;
            }
            // pegar
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'v') {
                e.preventDefault();
                // intentar desde clipboard API
                if (navigator.clipboard && navigator.clipboard.readText) {
                    navigator.clipboard.readText().then(text => {
                        pasteInto(active, text);
                    }).catch(()=>{
                        pasteInto(active, clipboard);
                    });
                } else {
                    pasteInto(active, clipboard);
                }
                return;
            }
        });

        function moveTo(r, c) {
            const rows = table.tBodies[0].rows;
            if (r < 0) r = 0;
            if (r >= rows.length) r = rows.length -1;
            const row = rows[r];
            if (!row) return;
            if (c < 0) c = 0;
            if (c >= row.cells.length) c = row.cells.length -1;
            const cell = row.cells[c];
            if (!cell) return;
            setActive(cell);
        }

        function highlightCopy(td) {
            td.classList.add('excel-copy-highlight');
            setTimeout(()=> td.classList.remove('excel-copy-highlight'), 800);
        }

        function pasteInto(td, text) {
            if (!isEditableCell(td)) return;
            if (text === undefined) return;
            // Si td contiene input oculto o campo, reemplazar
            td.textContent = text;
        }

        function startEdit(td) {
            if (!isEditableCell(td)) return;
            if (td.classList.contains('editing')) return;
            td.classList.add('editing');
            const prev = td.textContent.trim();
            td.innerHTML = '';
            const input = document.createElement('input');
            input.type = 'text';
            input.value = prev;
            input.className = 'excel-input';
            td.appendChild(input);
            input.focus();
            input.select();

            function accept() {
                td.classList.remove('editing');
                const v = input.value;
                td.textContent = v;
                setActive(td);
            }
            function cancel() {
                td.classList.remove('editing');
                td.textContent = prev;
                setActive(td);
            }

            input.addEventListener('keydown', function(e){
                if (e.key === 'Enter') { e.preventDefault(); accept(); }
                else if (e.key === 'Escape') { e.preventDefault(); cancel(); }
            });

            input.addEventListener('blur', function(){ accept(); });
        }

        // doble clic para editar
        table.addEventListener('dblclick', function(e){
            const td = e.target.closest('td');
            if (!td) return;
            startEdit(td);
        });

        // click en cabecera para ordenar (toggle asc/desc)
        const thead = table.querySelector('thead');
        if (thead) {
            thead.addEventListener('click', function(e){
                const th = e.target.closest('th');
                if (!th) return;
                const colIndex = Array.from(th.parentElement.children).indexOf(th);
                sortByColumn(table, colIndex);
            });
        }

        function sortByColumn(table, colIndex) {
            const tbody = table.tBodies[0];
            const rows = Array.from(tbody.rows);
            const asc = table.dataset.sortDir !== 'asc';
            rows.sort((a,b)=>{
                const A = (a.cells[colIndex] && a.cells[colIndex].textContent.trim()) || '';
                const B = (b.cells[colIndex] && b.cells[colIndex].textContent.trim()) || '';
                const numA = parseFloat(A.replace(/[^0-9.-]+/g, ''));
                const numB = parseFloat(B.replace(/[^0-9.-]+/g, ''));
                if (!isNaN(numA) && !isNaN(numB)) return asc ? numA - numB : numB - numA;
                return asc ? A.localeCompare(B, undefined, {numeric:true}) : B.localeCompare(A, undefined, {numeric:true});
            });
            rows.forEach(r=> tbody.appendChild(r));
            table.dataset.sortDir = asc ? 'asc' : 'desc';
        }

        // inicializar primera celda activa
        const firstRow = table.tBodies[0] && table.tBodies[0].rows[0];
        if (firstRow) {
            const firstCell = firstRow.cells[0];
            if (firstCell) setActive(firstCell);
        }
    }

    // Función pública para inicializar excel-grids dentro de un contenedor
    window.initExcelGrids = function(root=document) {
        (root.querySelectorAll ? root : document).querySelectorAll('table.excel-grid').forEach(tbl => makeExcelGrid(tbl));
    };

    // Auto-init al cargar la página completa
    document.addEventListener('DOMContentLoaded', function(){
        window.initExcelGrids(document);
    });
})();
