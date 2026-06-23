function SearchForm({ruc, setRuc, periodo, setPeriodo, periodos, onSearch}) {    


    const submit=(e)=>{

        e.preventDefault()

        if (!ruc.trim()) {
            alert(
                "Ingrese su número de RUC"
            );
            return;
        }


        if (!periodo) {
            alert(
                "Seleccione un período"
            );
            return;
        }

        onSearch()

    }

    return(

        <form
            className="form"
            onSubmit={submit}
        >

            <input
                className="input"
                value={ruc}
                onChange={(e)=>setRuc(
                    e.target.value
                )}
                placeholder="Ingrese su número de RUC"
            />

            <select
                value={periodo}
                onChange={(e) => setPeriodo(e.target.value)}
                >
                <option value="">Seleccione un mes</option>

                {periodos.map((p) => (
                    <option
                    key={p.value}
                    value={p.value}
                    >
                    {p.label}
                    </option>
                ))}
            </select>

            <button
                className="button"
                type="submit"
            >
                Buscar
            </button>

        </form>

    )

}

export default SearchForm