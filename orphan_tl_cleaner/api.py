import os
import re

from .i18n import TRANSLATIONS


class Cleaner:
    @staticmethod
    def load_identifiers(lint_file):
        with open(lint_file, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = r'\(id (\w+)\)'
        # Usamos set() para eliminar duplicados y hacer búsquedas instantáneas
        return list(set(re.findall(pattern, content)))

    @staticmethod
    def process_file(content, identifiers, language, comment_blocks):
        if not identifiers:
            return content

        # 1. Creamos un grupo de captura con todos los identificadores: (id1|id2|id3...)
        # Esto permite que el motor de Regex busque cualquiera de ellos en una sola pasada.
        escaped_ids = "|".join(re.escape(i) for i in identifiers)
        
        # 2. Expresión regular que coincide con el bloque completo de traducción de Ren'Py
        pattern = rf'(?m)^translate\s+{re.escape(language)}\s+({escaped_ids}):(.*?)^(?=\S|\Z)'
        compiled_pattern = re.compile(pattern, re.DOTALL)

        # 3. Función interna que decidirá qué hacer cada vez que encuentre un bloque válido
        def replacer(match):
            bloque_completo = match.group(0)
            if comment_blocks:
                lineas_bloque = bloque_completo.strip().split("\n")
                lineas_modificadas = ["# " + linea if linea.strip() else "" for linea in lineas_bloque]
                return "\n".join(lineas_modificadas) + "\n\n"
            else:
                return ""

        # Reemplaza todos los bloques huérfanos del archivo en un único escaneo
        return compiled_pattern.sub(replacer, content)

    def run_tool(self, directory, lint_file, language, comment_blocks, locale='es_ES'):
        identifiers = self.load_identifiers(lint_file)
        if not identifiers:
            return TRANSLATIONS.get(locale, TRANSLATIONS['es_ES']).get('error_no_identifiers', 'No identifiers found.')

        t = TRANSLATIONS.get(locale, TRANSLATIONS['es_ES'])
        files_processed = []

        # El bucle sigue procesando los archivos uno por uno
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.rpy') or file.endswith('.rpym'):
                    filepath = os.path.join(root, file)
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Ahora este paso unitario es drásticamente más rápido
                    updated_content = self.process_file(content, identifiers, language, comment_blocks)

                    if updated_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(updated_content)
                        files_processed.append(filepath)

        if files_processed:
            return t.get('processed_header', 'Processed files:\n{files}').format(files="\n".join(files_processed))
        else:
            return t.get('no_files_processed', 'No files were found to process.')
