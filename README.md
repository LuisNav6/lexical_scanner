📚 **Escáner de Tokens**

Este código implementa un escáner de tokens para un lenguaje de programación. Utiliza un autómata finito determinista (DFA) para analizar un archivo fuente y dividirlo en tokens.

🔠 **Tipos de Tokens**
- 🏁 `ENDFILE` y `ERROR`: Control y errores.
- 📝 Palabras reservadas como `IF`, `ELSE`, `WHILE`, etc.
- 🔢 Números enteros y reales (`NUM_INT`, `NUM_REAL`).
- ➕➖ Operadores aritméticos y relacionales.
- ⚙️ Símbolos especiales como paréntesis, llaves, comas, etc.
- 📝 Comentarios tanto de una sola línea como de múltiples líneas.

🔍 **Funciones Principales**
- `getNextChar()`: Obtiene el siguiente carácter no en blanco de la línea actual.
- `ungetNextChar()`: Retrocede un carácter en la línea actual.
- `reservedLookup(s)`: Busca si un identificador es una palabra reservada.
- `getToken()`: Analiza el archivo fuente y devuelve el siguiente token.

🛠️ **Prueba del Escáner**
- Lee un archivo fuente y llama a `getToken()` hasta el final del archivo.
- Maneja errores léxicos, como identificadores no válidos.

Este código proporciona la base para analizar programas escritos en el lenguaje definido.
