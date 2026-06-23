import { useState, useEffect } from "react";
import SearchForm from "./components/SearchForm"
import ResultadoCard from "./components/ResultadoCard"
import UltimaActualizacion from "./components/UltimaActualizacion";
import api from "./services/api"



function App(){
    const [ruc, setRuc] = useState("");
    const [periodo, setPeriodo] = useState("");
    const [periodos, setPeriodos] = useState([]);
    const [datos, setDatos] = useState(null);

    useEffect(() => {
        
        async function cargarPeriodos() {
            
            const response = await api.get(
                "/periodos"
            );
            
            setPeriodos(
                response.data
            );
    
        }
    
        cargarPeriodos();
        
    }, []);
    
    async function buscar(){

        try{

            const response=await api.get(
                `/consulta?ruc=${ruc}&periodo=${periodo}`
            )

            setDatos(
                response.data
            )

        }

        catch(error){

            console.log(error);

            setDatos(null);

            alert(
                "No se encontraron registros"
            )

        }

    }

    return(

        <div className="container">

            <h1 className="title">

                Seguimiento de pagos docentes

            </h1>

            <UltimaActualizacion />

            <div className="card">

                <SearchForm
                    ruc={ruc}
                    setRuc={setRuc}
                    periodo={periodo}
                    setPeriodo={setPeriodo}
                    periodos={periodos}
                    onSearch={buscar}
                />

            </div>

            {datos && (

                <ResultadoCard
                    datos={datos}
                />

            )}

        </div>

    )

}

export default App