# Ejercicio: Orquestador concurrente de modelos

Notas de preparación del pre-ejercicio del Módulo 1 (Arquitectura asíncrona con Python 3.12).

## 1. El problema, sin código

Imaginate el backend de un chat. Llega una pregunta y querés consultar tres modelos (GPT, Claude, Llama local) para quedarte con las respuestas. Hay cuatro restricciones, y cada una se corresponde con algo que ya vimos:

| Lo que pide el ejercicio | Por qué existe | Sección del doc |
|---|---|---|
| Tres corrutinas con `await asyncio.sleep(...)` de distinta duración | Simulan la latencia de red de cada proveedor, sin llamar a ninguno de verdad | 2 |
| Dispararlas "a la vez" con `gather` | Si las esperás una por una, tardás la suma de las tres. Con `gather`, tardás lo de la más lenta | 3 |
| Timeout de 2 s | Un proveedor colgado no puede dejar al usuario esperando para siempre | 4 |
| Semáforo de 2, con 10 simulaciones | Evita pegarle al proveedor con 10 llamadas simultáneas (el `429`) | 4 |

Los criterios de aceptación son la forma de comprobar que lo hiciste bien: nada de `time.sleep`, que en los logs se vea que arrancan casi juntas, y que el `TimeoutError` no rompa el programa.

### Dos puntos del enunciado que son ambiguos

Conviene resolverlos antes de escribir, porque se contradicen un poco:

- **Timeout "a la ejecución total" vs. "si alguna llamada tarda más".** Son dos cosas distintas. Un timeout alrededor de todo el `gather` corta todo junto cuando se cumplen los 2 s. Un timeout por llamada corta solo a la lenta. La sección 4 del doc muestra dónde cambia el comportamiento.
- **"Las tareas inician casi al mismo tiempo" vs. semáforo de 2.** Con `Semaphore(2)` solo 2 pueden estar *ejecutándose* a la vez. Las otras 8 se crean juntas, pero esperan permiso. Hay que pensar qué mostrar en los logs para que quede claro quién arrancó cuándo y quién esperó.

Consecuencia adicional: si 10 llamadas de ~1 s van de a 2, son unos 5 s en total, y con un timeout global de 2 s no van a llegar a terminar. No es un bug propio, es algo para decidir (y probablemente para consultarle al curso cuál es la intención).

## 2. Nombre del archivo

La convención es la de PEP 8 para módulos: **minúsculas, palabras separadas con guion bajo, sin espacios ni guiones medios ni tildes**. Por ejemplo:

```
orquestador_modelos.py
```

Dos cuidados:

- No llamarlo igual que un módulo que se va a importar (`asyncio.py`, `time.py`, `random.py`). Python importaría ese archivo en lugar del módulo de la librería estándar y aparecen errores raros.
- Un nombre con guion medio (`orquestador-modelos.py`) funciona para ejecutarlo, pero no se puede importar desde otro archivo.

Entorno del paso 1, en Windows (de memoria, verificar la versión instalada con `python --version` si `py -3.12` no anda):

```
py -3.12 -m venv .venv
.venv\Scripts\activate
```

Patrón de arranque (sección 3 del doc): una `async def main()` y, al final:

```python
if __name__ == "__main__":
    asyncio.run(main())
```

## 3. Cómo seguir

Armarlo uno mismo y revisar la versión que corra contra los tres criterios de aceptación. Si hay un bloqueo, anotar qué se esperaba que pasara y qué pasó realmente.

## Fuentes

- [PEP 8, nombres de módulos](https://peps.python.org/pep-0008/#package-and-module-names)
- [venv, documentación de Python 3.12](https://docs.python.org/3.12/library/venv.html)