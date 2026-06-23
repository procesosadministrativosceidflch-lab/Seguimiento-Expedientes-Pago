import { ETAPAS } from "../constants/etapas";

function Timeline({ estadoActual, lineaTiempo }) {

    const etapaActualIndex = Number(estadoActual);

    return (

        <div className="timeline">

            {ETAPAS.map((etapa, index) => {

                const completada =
                    index <= etapaActualIndex;

                const fechaEncontrada =
                    lineaTiempo.find(
                        item => item.etapa === etapa
                    );

                return (

                    <div
                        key={index}
                        className="timeline-step"
                    >

                        <div
                            className={`timeline-circle ${
                                completada
                                    ? "completed"
                                    : ""
                            }`}
                        >
                            {completada ? "✓" : ""}
                        </div>

                        {index < ETAPAS.length - 1 && (

                            <div
                                className={`timeline-line ${
                                    index <
                                    etapaActualIndex
                                        ? "completed"
                                        : ""
                                }`}
                            />

                        )}

                        <div className="timeline-content">

                            <div className="timeline-title">
                                {etapa}
                            </div>

                            <div className="timeline-date">

                                {
                                    fechaEncontrada?.fecha ||
                                    ""
                                }

                            </div>

                        </div>

                    </div>

                );

            })}

        </div>

    );

}

export default Timeline;