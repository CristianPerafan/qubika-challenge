# **Reto Empresarial Qubika**

## **Introducción**

Este proyecto tiene como objetivo desarrollar un sistema de *Retrieval-Augmented Generation* (RAG) que genere respuestas utilizando un *Large Language Model* (LLM). El sistema combina información contextual procesada y almacenada en una base de datos vectorial, con datos provenientes de documentos de noticias recopilados mediante técnicas avanzadas de *web scraping*. La información procesada se utiliza para enriquecer las consultas realizadas al modelo, garantizando respuestas relevantes y precisas.

El proyecto está estructurado en los siguientes módulos principales:  
1. **Scraping de datos:** Extracción de información desde sitios web relevantes.  
2. **Base de datos vectorial:** Almacenamiento optimizado para una recuperación eficiente de información.  
3. **Generación de respuestas:** Procesamiento avanzado mediante LLM.  
4. **Interfaz de usuario:** Plataforma interactiva para realizar consultas y visualizar datos.  

Este sistema fue diseñado con el propósito de explorar y aplicar tecnologías de inteligencia artificial, mejorando el acceso y la utilización de información estructurada en escenarios prácticos y empresariales.

## **Reporte Detallado**

Para más información sobre el funcionamiento del sistema, consulta el archivo [`report.md`](./report/report.md).

## **Arquitectura**

A continuación, se presenta un diagrama que ilustra la arquitectura del sistema:  

![Arquitectura](./report/img/diagram.png)

## **Configuración del Proyecto**

El proyecto puede configurarse de dos maneras: utilizando Docker o mediante una instalación local.

### **Configuración Local**

1. Clona el repositorio:
    ```bash
    git clone https://github.com/CristianPerafan/qubika-challenge.git
    ```

2. Crea un entorno virtual:
    ```bash
    python -m venv venv
    ```

3. Activa el entorno virtual:  
   **Windows:**
    ```bash
    venv\Scripts\activate
    ```  
   **Linux:**
    ```bash
    source venv/bin/activate
    ```

4. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

5. Ejecuta Chroma en un contenedor Docker para permitir la comunicación del RAG con la base de datos vía HTTP:  
    ```bash
    docker pull chromadb/chroma
    docker run -p 8000:8000 chromadb/chroma
    ```

6. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:
    ```env
    OPENAI_API_KEY=sk-XXXXXXXX
    CHROMA_HOST=localhost
    CHROMA_PORT=8000
    ```

7. Ejecuta la interfaz web:
    ```bash
    streamlit run app.py
    ```

8. Accede a la interfaz web en:  
   `http://localhost:8501`

### **Configuración con Docker Compose**

1. Clona el repositorio:
    ```bash
    git clone https://github.com/CristianPerafan/qubika-challenge.git
    ```

2. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:
    ```env
    OPENAI_API_KEY=sk-XXXXXXXX
    CHROMA_HOST=chroma
    CHROMA_PORT=8000
    ```

3. Inicia el proyecto utilizando *Docker Compose*:
    ```bash
    docker-compose up --build
    ```

4. Accede a la interfaz web en:  
   `http://localhost:8501`







