import { useEffect, useState } from "react";
import api from "../services/api";

function UltimaActualizacion() {

    const [sync, setSync] = useState(null);

    useEffect(() => {

        async function cargarSync() {

            try {

                const response = await api.get(
                    "/ultima-sincronizacion"
                );

                setSync(
                    response.data
                );

            }

            catch (error) {

                console.log(error);

            }

        }

        cargarSync();

    }, []);

    if (!sync) {

        return null;

    }

    const fecha = new Date(
        sync.fecha_fin
    ).toLocaleString(
        "es-PE"
    );

    return (

        <div className="sync-card">

            <strong>
                Última actualización:
            </strong>

            {" "}

            {fecha}

        </div>

    );

}

export default UltimaActualizacion;