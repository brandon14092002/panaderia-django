document.addEventListener("DOMContentLoaded", function() {
    try {
        console.log("✅ pedido_admin.js cargado correctamente");

        const tipoSelect = document.getElementById("id_tipo");
        const saborSelect = document.getElementById("id_sabor");

        const saboresNormal = [
            {value: "naranja", text: "Naranja"},
            {value: "vainilla", text: "Vainilla"},
            {value: "red_velvet", text: "Red Velvet"},
            {value: "banano", text: "Banano"}
        ];

        const saboresRelleno = [
            {value: "relleno", text: "Relleno"},
            {value: "humedo", text: "Húmedo"},
            {value: "tres_leches", text: "Tres Leches"},
            {value: "selva_negra", text: "Selva Negra"},
            {value: "dos_amores", text: "Dos Amores"},
            {value: "cheesecake", text: "Cheesecake"},
            {value: "leche_asada", text: "Leche Asada"},
            {value: "tiramisu", text: "Tiramisú"}
        ];

        function actualizarSabores() {
            const tipo = tipoSelect.value;
            let opciones = [];

            if (tipo === "normal") {
                opciones = saboresNormal;
            } else if (tipo === "relleno") {
                opciones = saboresRelleno;
            }

            // Limpia las opciones actuales
            saborSelect.innerHTML = "";

            // Siempre agrega la opción vacía primero
            const emptyOption = document.createElement("option");
            emptyOption.value = "";
            emptyOption.textContent = "---------";
            saborSelect.appendChild(emptyOption);

            // Agrega las nuevas opciones
            opciones.forEach(opt => {
                const option = document.createElement("option");
                option.value = opt.value;
                option.textContent = opt.text;
                saborSelect.appendChild(option);
            });

            console.log("🔄 Opciones de sabor actualizadas:", opciones);
        }

        if (tipoSelect && saborSelect) {
            tipoSelect.addEventListener("change", actualizarSabores);
            actualizarSabores(); // inicializar al cargar
        } else {
            console.warn("⚠️ No se encontraron los campos 'tipo' o 'sabor'");
        }
    } catch (error) {
        console.error("❌ Error en pedido_admin.js:", error);
    }
});