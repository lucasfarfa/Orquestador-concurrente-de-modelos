import asyncio
import time

inicio = time.perf_counter()

TIMEOUT_TOTAL = 2.0         # segundos, a la ejecución total
MAX_CONCURRENTES = 2        # permisos del semáforo
CANTIDAD_LLAMADAS = 10      # cuántas simulaciones se intentan disparar


def log(mensaje: str) -> None:
    print(f"[{time.perf_counter() - inicio:.2f}s] {mensaje}")


# Paso 2: tres corrutinas, cada una con su latencia simulada
async def gpt_4_call(numero: int, sem: asyncio.Semaphore) -> str:
    log(f"GPT #{numero}: pide permiso")
    async with sem:
        log(f"GPT #{numero}: INICIO")
        await asyncio.sleep(1.0)
        log(f"GPT #{numero}: FIN")
    return f"Respuesta GPT #{numero}"


async def claude_3_call(numero: int, sem: asyncio.Semaphore) -> str:
    log(f"CLAUDE #{numero}: pide permiso")
    async with sem:
        log(f"CLAUDE #{numero}: INICIO")
        await asyncio.sleep(0.5)
        log(f"CLAUDE #{numero}: FIN")
    return f"Respuesta Claude #{numero}"


async def local_llama_call(numero: int, sem: asyncio.Semaphore) -> str:
    log(f"LOCAL #{numero}: pide permiso")
    async with sem:
        log(f"LOCAL #{numero}: INICIO")
        await asyncio.sleep(1.2)
        log(f"LOCAL #{numero}: FIN")
    return f"Respuesta Local #{numero}"


# Pasos 3, 4 y 5: gather + timeout total + semáforo
async def orchestrator() -> list:
    sem = asyncio.Semaphore(MAX_CONCURRENTES)    # UN solo semáforo compartido
    modelos = [gpt_4_call, claude_3_call, local_llama_call]
    # Reparte las N simulaciones entre los tres modelos
    tareas = [modelos[i % 3](i + 1, sem) for i in range(CANTIDAD_LLAMADAS)]

    results = []
    try:
        async with asyncio.timeout(TIMEOUT_TOTAL):
            results = await asyncio.gather(*tareas, return_exceptions=True)
    except TimeoutError:
        log(f"ERROR: la ejecución total superó {TIMEOUT_TOTAL}s")
    return results


async def main() -> None:
    resultados = await orchestrator()
    log(f"Resultados recibidos: {len(resultados)}")


if __name__ == "__main__":
    asyncio.run(main())