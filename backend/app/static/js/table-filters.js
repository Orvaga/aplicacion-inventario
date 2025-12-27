/**
 * TableFilter: sistema de búsqueda, filtros y paginación client-side para tablas
 * Uso: new TableFilter('table-id', { searchable: true, pageable: true, rowsPerPage: 10 })
 */
class TableFilter {
    constructor(tableId, options = {}) {
        this.table = document.getElementById(tableId);
        if (!this.table) return;

        this.tbody = this.table.querySelector('tbody');
        this.rows = Array.from(this.tbody.querySelectorAll('tr'));
        this.filteredRows = [...this.rows];

        // Opciones
        this.options = {
            searchable: options.searchable !== false,
            pageable: options.pageable !== false,
            rowsPerPage: options.rowsPerPage || 10,
            searchColumns: options.searchColumns || [], // [] = todas las columnas
        };

        this.currentPage = 1;
        this.totalPages = 1;

        // Inicializar
        if (this.options.searchable) this.initSearch();
        if (this.options.pageable) this.initPagination();
        this.updateTable();
    }

    initSearch() {
        // Buscar o crear contenedor de controles
        let controls = this.table.parentElement.querySelector('.table-controls');
        if (!controls) {
            controls = document.createElement('div');
            controls.className = 'table-controls';
            this.table.parentElement.insertBefore(controls, this.table);
        }

        // Crear campo de búsqueda (o reutilizar existente)
        let searchDiv = controls.querySelector('.table-search');
        // Si la plantilla marca que no quiere búsqueda local, no crear ni enlazar input local
        const noLocal = controls.dataset && controls.dataset.noLocalSearch === 'true';
        if (!searchDiv && !noLocal) {
            searchDiv = document.createElement('div');
            searchDiv.className = 'table-search';
            const input = document.createElement('input');
            input.type = 'text';
            input.placeholder = '🔍 Buscar...';
            input.addEventListener('keyup', (e) => this.filterRows(e.target.value));
            searchDiv.appendChild(input);
            controls.insertBefore(searchDiv, controls.firstChild);
        } else if (!noLocal) {
            // si existe un input ya creado por la plantilla, enlazamos el listener
            const existingInput = searchDiv.querySelector('input');
            if (existingInput) {
                existingInput.addEventListener('keyup', (e) => this.filterRows(e.target.value));
            }
        } else {
            // Si no local pero existe el input global (cabecera), enlazarlo para filtrar esta tabla
            const globalInput = document.getElementById('search-input');
            if (globalInput) {
                globalInput.addEventListener('keyup', (e) => this.filterRows(e.target.value));
            }
        }

        // Crear botones de acciones
        let actionsDiv = controls.querySelector('.table-actions');
        if (!actionsDiv) {
            actionsDiv = document.createElement('div');
            actionsDiv.className = 'table-actions';
            
            // Botones: crear export y clear solo si la plantilla habilita explícitamente
            const enableExport = controls.dataset && controls.dataset.enableExport === 'true';
            const enableClear = controls.dataset && controls.dataset.enableClear === 'true';
            if (enableExport) {
                const exportBtn = document.createElement('button');
                exportBtn.className = 'btn-export';
                exportBtn.textContent = '📥 Exportar CSV';
                exportBtn.addEventListener('click', () => this.exportToCSV());
                actionsDiv.appendChild(exportBtn);
            }

            // Botón limpiar filtro: crear solo si la plantilla habilita explícitamente
            if (enableClear) {
                const clearBtn = document.createElement('button');
                clearBtn.className = 'btn-clear-filter';
                clearBtn.textContent = '✕ Limpiar';
                clearBtn.addEventListener('click', () => {
                    const input = (searchDiv && searchDiv.querySelector('input')) || document.getElementById('search-input');
                    if (input) input.value = '';
                    this.filterRows('');
                });
                actionsDiv.appendChild(clearBtn);
            }

            controls.appendChild(actionsDiv);
        } else {
            // enlazar acciones si los botones ya existen en la plantilla
            const exportBtn = actionsDiv.querySelector('.btn-export');
            if (exportBtn) exportBtn.addEventListener('click', () => this.exportToCSV());
            const clearBtn = actionsDiv.querySelector('.btn-clear-filter');
            if (clearBtn) clearBtn.addEventListener('click', () => {
                const input = (searchDiv && searchDiv.querySelector('input')) || document.getElementById('search-input');
                if (input) input.value = '';
                this.filterRows('');
            });
        }
    }

    initPagination() {
        // Crear contenedor de paginación
        let pagination = this.table.parentElement.querySelector('.pagination-controls');
        if (!pagination) {
            pagination = document.createElement('div');
            pagination.className = 'pagination-controls';
            this.table.parentElement.appendChild(pagination);
        }

        // Info de paginación
        let infoDiv = pagination.querySelector('.pagination-info');
        if (!infoDiv) {
            infoDiv = document.createElement('div');
            infoDiv.className = 'pagination-info';
            pagination.insertBefore(infoDiv, pagination.firstChild);
        }

        // Controles de paginación
        let navDiv = pagination.querySelector('.pagination-nav');
        if (!navDiv) {
            navDiv = document.createElement('div');
            navDiv.className = 'pagination-nav';

            // Selector de filas por página
            const rowsPerPageDiv = document.createElement('div');
            rowsPerPageDiv.className = 'rows-per-page';
            const label = document.createElement('span');
            label.textContent = 'Filas por página:';
            const select = document.createElement('select');
            [10, 25, 50, 100].forEach(n => {
                const option = document.createElement('option');
                option.value = n;
                option.textContent = n;
                if (n === this.options.rowsPerPage) option.selected = true;
                select.appendChild(option);
            });
            select.addEventListener('change', (e) => {
                this.options.rowsPerPage = parseInt(e.target.value);
                this.currentPage = 1;
                this.updateTable();
            });
            rowsPerPageDiv.appendChild(label);
            rowsPerPageDiv.appendChild(select);
            navDiv.appendChild(rowsPerPageDiv);

            // Botones de navegación
            const prevBtn = document.createElement('button');
            prevBtn.textContent = '← Anterior';
            prevBtn.addEventListener('click', () => this.prevPage());
            navDiv.appendChild(prevBtn);

            const nextBtn = document.createElement('button');
            nextBtn.textContent = 'Siguiente →';
            nextBtn.addEventListener('click', () => this.nextPage());
            navDiv.appendChild(nextBtn);

            pagination.appendChild(navDiv);
        }
    }

    filterRows(searchTerm) {
        searchTerm = searchTerm.toLowerCase().trim();
        this.filteredRows = this.rows.filter(row => {
            const cells = Array.from(row.querySelectorAll('td'));
            const columnsToSearch = this.options.searchColumns.length > 0 
                ? cells.filter((_, i) => this.options.searchColumns.includes(i))
                : cells.slice(0, -1); // Excluir última columna (acciones)
            
            return columnsToSearch.some(cell => 
                cell.textContent.toLowerCase().includes(searchTerm)
            );
        });

        this.currentPage = 1;
        this.updateTable();
    }

    updateTable() {
        // Calcular paginación
        this.totalPages = Math.ceil(this.filteredRows.length / this.options.rowsPerPage) || 1;
        const start = (this.currentPage - 1) * this.options.rowsPerPage;
        const end = start + this.options.rowsPerPage;
        const visibleRows = this.filteredRows.slice(start, end);

        // Mostrar/ocultar filas
        this.rows.forEach(row => row.classList.add('hidden'));
        visibleRows.forEach(row => row.classList.remove('hidden'));

        // Mostrar mensaje si no hay resultados
        const tbody = this.table.querySelector('tbody');
        let noResults = tbody.querySelector('.no-results');
        if (this.filteredRows.length === 0) {
            if (!noResults) {
                noResults = document.createElement('tr');
                noResults.className = 'no-results';
                noResults.innerHTML = '<td colspan="100" style="padding: 30px; text-align: center; color: #7f8c8d;">No se encontraron resultados</td>';
                tbody.appendChild(noResults);
            }
        } else if (noResults) {
            noResults.remove();
        }

        // Actualizar controles de paginación
        if (this.options.pageable) {
            this.updatePaginationControls();
        }
    }

    updatePaginationControls() {
        const pagination = this.table.parentElement.querySelector('.pagination-controls');
        if (!pagination) return;

        // Actualizar info
        const infoDiv = pagination.querySelector('.pagination-info');
        const from = this.filteredRows.length === 0 ? 0 : (this.currentPage - 1) * this.options.rowsPerPage + 1;
        const to = Math.min(this.currentPage * this.options.rowsPerPage, this.filteredRows.length);
        const total = this.filteredRows.length;
        infoDiv.textContent = `Mostrando ${from}-${to} de ${total} registros`;

        // Actualizar botones
        const prevBtn = pagination.querySelector('.pagination-nav button:nth-child(2)');
        const nextBtn = pagination.querySelector('.pagination-nav button:nth-child(3)');
        if (prevBtn) prevBtn.disabled = this.currentPage === 1;
        if (nextBtn) nextBtn.disabled = this.currentPage >= this.totalPages;
    }

    nextPage() {
        if (this.currentPage < this.totalPages) {
            this.currentPage++;
            this.updateTable();
            // Scroll hacia la tabla
            this.table.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    prevPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.updateTable();
            this.table.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    exportToCSV() {
        let csv = [];
        
        // Encabezados
        const headers = Array.from(this.table.querySelectorAll('thead th'))
            .map(th => th.textContent.trim())
            .slice(0, -1); // Excluir columna de acciones
        csv.push(headers.join(','));

        // Filas visibles
        this.filteredRows.forEach(row => {
            const cells = Array.from(row.querySelectorAll('td'))
                .slice(0, -1) // Excluir columna de acciones
                .map(td => {
                    let text = td.textContent.trim();
                    // Escapar comillas y envolver en comillas si contiene coma
                    if (text.includes(',') || text.includes('"') || text.includes('\n')) {
                        text = '"' + text.replace(/"/g, '""') + '"';
                    }
                    return text;
                });
            csv.push(cells.join(','));
        });

        // Crear y descargar archivo
        const csvContent = csv.join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        
        // Nombre del archivo con fecha
        const now = new Date();
        const timestamp = now.getFullYear() + '-' + 
                         String(now.getMonth() + 1).padStart(2, '0') + '-' +
                         String(now.getDate()).padStart(2, '0') + '_' +
                         String(now.getHours()).padStart(2, '0') +
                         String(now.getMinutes()).padStart(2, '0');
        const tableTitle = this.table.id || 'datos';
        
        link.setAttribute('href', url);
        link.setAttribute('download', `${tableTitle}_${timestamp}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Función pública para inicializar tablas filterable dentro de un contenedor
window.initTableFilters = function(root=document) {
    (root.querySelectorAll ? root : document).querySelectorAll('table.filterable').forEach(table => {
        if (!table.id) {
            table.id = 'table-' + Math.random().toString(36).substr(2, 9);
        }
        new TableFilter(table.id, {
            searchable: true,
            pageable: true,
            rowsPerPage: 10
        });
    });
};

// Inicialización al cargar la página completa
document.addEventListener('DOMContentLoaded', function() {
    window.initTableFilters(document);
});
