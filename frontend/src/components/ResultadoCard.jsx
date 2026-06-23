import Timeline from "./Timeline";
import { ETAPAS } from "../constants/etapas";

function ResultadoCard({ datos }) {

    if (datos.expedientes.length === 0) {

        return (
            <div className="card">
                <h2>
                    {datos.docente}
                </h2>

                <p>
                    No se encontraron expedientes para el período seleccionado.
                </p>

            </div>

        );

    }

    return (

        <div className="card">

            <h2>
                {datos.docente}
            </h2>

            <p>
                Cantidad de expedientes:
                {" "}
                {datos.expedientes.length}
            </p>

            <br/>

            {datos.expedientes.map((exp,index)=>(

                console.log(
                    "Expediente:",
                    exp.numero_expediente,
                    "Estado:",
                    exp.estado_actual,
                    "Tipo:",
                    typeof exp.estado_actual
                ),

                <div
                    key={index}
                    className="expediente"
                >

                    <p>

                        <strong>
                            Expediente:
                        </strong>

                        {" "}

                        {exp.numero_expediente}

                    </p>

                    <p className="estado">

                        Estado: {ETAPAS[exp.estado_actual]}

                    </p>

                    <p className="fecha">

                        {
                            exp.estado_actual === 5 &&
                            exp.fecha_estimada_pago && (
                                <p className="fecha">
                                Fecha probable: {exp.fecha_estimada_pago}
                                </p>
                            )
                        }

                    </p>
                
                    <h4>Línea de tiempo</h4>

                    <Timeline
                        estadoActual={exp.estado_actual}
                        lineaTiempo={exp.linea_tiempo}
                    />

                </div>

            ))}

        </div>

    )

}

export default ResultadoCard