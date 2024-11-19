# **RETO EMPRESARIAL QUBIKA**

## **Configuración**

1. Clonar el repositorio
    ```bash
    git clone https://github.com/CristianPerafan/qubika-challenge.git
    ```
2. Crear un entorno virtual
    ```bash
    python -m venv venv
    ```
3. Activar el entorno virtual

    Windows:
    ```bash
    venv\Scripts\activate
    ```
    Linux:
    ```bash
    source venv/bin/activate
    ```

4. Instalar dependencias
    ```bash
    pip install -r requirements.txt
    ```
   
5. Crear un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno
    ```env
   OPENAI_API_KEY=sk-XXXXXXXX
   CHROMA_HOST=XXXXXXXX
   CHROMA_PORT=XXXX
   ```


