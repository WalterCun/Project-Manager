"""
Template Parser - Parser de expresiones en plantillas.

Parsea expresiones como:
- {{variable}}
- {{DATE.now()}}
- {{#if condition}}...{{/if}}
- {{#for item in array}}...{{/for}}
"""

import re
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class Token:
    """Representa un token parseado."""
    type: str  # 'text', 'variable', 'function', 'if', 'for', 'end_if', 'end_for', etc
    content: str
    line: int = 0
    col: int = 0


class TemplateParser:
    """Parser de templates con soporte para expresiones y estructuras de control."""

    # Patrones regex
    VARIABLE_PATTERN = r'\{\{([^#/}][^}]*)\}\}'  # {{variable}} o {{function()}}
    BLOCK_START_PATTERN = r'\{\{#(\w+)\s+([^}]*)\}\}'  # {{#if ...}} {{#for ...}}
    BLOCK_END_PATTERN = r'\{\{/(\w+)\}\}'  # {{/if}} {{/for}}
    ELSE_PATTERN = r'\{\{else\}\}'  # {{else}}
    ELIF_PATTERN = r'\{\{elif\s+([^}]*)\}\}'  # {{elif condition}}

    def __init__(self):
        """Inicializar parser."""
        pass

    def parse(self, template: str) -> List[Token]:
        """
        Parsear template en tokens.

        Args:
            template: String del template a parsear

        Returns:
            Lista de tokens
        """
        tokens = []
        position = 0
        line = 1
        col = 1

        while position < len(template):
            # Buscar próxima expresión
            match_var = re.search(self.VARIABLE_PATTERN, template[position:])
            match_block_start = re.search(self.BLOCK_START_PATTERN, template[position:])
            match_block_end = re.search(self.BLOCK_END_PATTERN, template[position:])
            match_else = re.search(self.ELSE_PATTERN, template[position:])
            match_elif = re.search(self.ELIF_PATTERN, template[position:])

            # Encontrar el match más cercano
            matches = [
                (match_var, 'variable') if match_var else None,
                (match_block_start, 'block_start') if match_block_start else None,
                (match_block_end, 'block_end') if match_block_end else None,
                (match_else, 'else') if match_else else None,
                (match_elif, 'elif') if match_elif else None,
            ]
            matches = [m for m in matches if m is not None]

            if not matches:
                # No hay más expresiones, agregar texto restante
                if position < len(template):
                    tokens.append(Token('text', template[position:], line, col))
                break

            # Ordenar por posición de inicio
            matches.sort(key=lambda x: x[0].start())
            closest_match, match_type = matches[0]

            # Agregar texto antes del match
            if closest_match.start() > 0:
                text_before = template[position:position + closest_match.start()]
                tokens.append(Token('text', text_before, line, col))
                # Actualizar línea y columna
                line += text_before.count('\n')
                if '\n' in text_before:
                    col = len(text_before.split('\n')[-1]) + 1
                else:
                    col += len(text_before)

            # Procesar el match
            if match_type == 'variable':
                content = closest_match.group(1).strip()
                # Detectar si es una función (contiene paréntesis)
                if '(' in content:
                    tokens.append(Token('function', content, line, col))
                else:
                    tokens.append(Token('variable', content, line, col))

            elif match_type == 'block_start':
                block_type = closest_match.group(1)  # 'if', 'for', 'switch', etc
                block_content = closest_match.group(2).strip()
                tokens.append(Token(f'start_{block_type}', block_content, line, col))

            elif match_type == 'block_end':
                block_type = closest_match.group(1)
                tokens.append(Token(f'end_{block_type}', '', line, col))

            elif match_type == 'else':
                tokens.append(Token('else', '', line, col))

            elif match_type == 'elif':
                condition = closest_match.group(1).strip()
                tokens.append(Token('elif', condition, line, col))

            # Actualizar posición
            position += closest_match.end()
            col += len(closest_match.group(0))

        return tokens

    def extract_variables(self, template: str) -> List[str]:
        """
        Extraer todas las variables del template.

        Args:
            template: String del template

        Returns:
            Lista de nombres de variables
        """
        variables = set()
        matches = re.finditer(self.VARIABLE_PATTERN, template)

        for match in matches:
            content = match.group(1).strip()
            # Si no tiene paréntesis, es una variable
            if '(' not in content:
                # Extraer solo el nombre de la variable (antes de cualquier operador)
                var_name = content.split()[0] if ' ' in content else content
                variables.add(var_name)

        return list(variables)

    def extract_functions(self, template: str) -> List[Tuple[str, List[str]]]:
        """
        Extraer todas las funciones del template.

        Args:
            template: String del template

        Returns:
            Lista de tuplas (nombre_funcion, [argumentos])
        """
        functions = []
        matches = re.finditer(self.VARIABLE_PATTERN, template)

        for match in matches:
            content = match.group(1).strip()
            # Si tiene paréntesis, es una función
            if '(' in content:
                func_match = re.match(r'([^(]+)\((.*)\)', content)
                if func_match:
                    func_name = func_match.group(1).strip()
                    args_str = func_match.group(2).strip()
                    # Parsear argumentos (simplificado)
                    args = [arg.strip().strip("'\"") for arg in args_str.split(',')] if args_str else []
                    functions.append((func_name, args))

        return functions

    def validate_syntax(self, template: str) -> Tuple[bool, List[str]]:
        """
        Validar sintaxis del template.

        Args:
            template: String del template

        Returns:
            Tupla (es_valido, lista_de_errores)
        """
        errors = []
        tokens = self.parse(template)

        # Stack para verificar bloques balanceados
        block_stack = []

        for token in tokens:
            if token.type.startswith('start_'):
                block_type = token.type.replace('start_', '')
                block_stack.append((block_type, token.line))
            elif token.type.startswith('end_'):
                block_type = token.type.replace('end_', '')
                if not block_stack:
                    errors.append(f"Línea {token.line}: Bloque {{{{/{block_type}}}}} sin apertura")
                else:
                    start_type, start_line = block_stack.pop()
                    if start_type != block_type:
                        errors.append(
                            f"Línea {token.line}: Esperaba {{{{/{start_type}}}}} pero encontró {{{{/{block_type}}}}}"
                        )

        # Verificar bloques sin cerrar
        for block_type, line in block_stack:
            errors.append(f"Línea {line}: Bloque {{{{#{block_type}}}}} sin cerrar")

        return len(errors) == 0, errors
