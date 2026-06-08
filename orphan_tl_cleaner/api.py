import os
import re

from .i18n import TRANSLATIONS


class Cleaner:
    @staticmethod
    def load_identifiers(lint_file):
        with open(lint_file, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = r'\(id (\w+)\)'
        return re.findall(pattern, content)

    @staticmethod
    def process_file(content, identifiers, language, comment_blocks):
        for identifier in identifiers:
            pattern = rf'(?m)^translate\s+{re.escape(language)}\s+{re.escape(identifier)}:(.*?)^(?=\S|\Z)'
            compiled_pattern = re.compile(pattern, re.DOTALL)
            bloque_match = compiled_pattern.search(content)
            if bloque_match:
                bloque_completo = bloque_match.group(0)
                if comment_blocks:
                    lineas_bloque = bloque_completo.strip().split("\n")
                    lineas_modificadas = ["# " + linea if linea.strip() else "" for linea in lineas_bloque]
                    bloque_modificado = "\n".join(lineas_modificadas) + "\n\n"
                else:
                    bloque_modificado = ""

                content = content.replace(bloque_completo, bloque_modificado)

        return content

    def run_tool(self, directory, lint_file, language, comment_blocks, locale='es_ES'):
        identifiers = self.load_identifiers(lint_file)
        if not identifiers:
            return TRANSLATIONS.get(locale, TRANSLATIONS['es_ES']).get('error_no_identifiers', 'No identifiers found.')

        t = TRANSLATIONS.get(locale, TRANSLATIONS['es_ES'])
        files_processed = []

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.rpy') or file.endswith('.rpym'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    updated_content = self.process_file(content, identifiers, language, comment_blocks)

                    if updated_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(updated_content)
                        files_processed.append(filepath)

        if files_processed:
            return t.get('processed_header', 'Processed files:\n{files}').format(files="\n".join(files_processed))
        else:
            return t.get('no_files_processed', 'No files were found to process.')
