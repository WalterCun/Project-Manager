"""
Template Renderer - Renderiza templates completos.

Coordina parser, evaluator y functions para renderizar templates.
"""

import re
from typing import Dict, Any
from .parser import TemplateParser, Token
from .evaluator import ExpressionEvaluator
from .functions import TemplateFunctions


class TemplateRenderer:
    """Renderizador de templates con soporte completo de expresiones."""

    def __init__(self, context: Dict[str, Any] = None):
        """
        Inicializar renderer.

        Args:
            context: Diccionario con parámetros y variables
        """
        self.context = context or {}
        self.parser = TemplateParser()
        self.evaluator = ExpressionEvaluator(self.context)
        self.functions = TemplateFunctions(self.context)

    def render(self, template: str, params: Dict[str, Any] = None) -> str:
        """
        Renderizar template completo.

        Args:
            template: String del template
            params: Parámetros adicionales (se merge con context)

        Returns:
            Template renderizado
        """
        # Merge params con context
        if params:
            self.context.update(params)
            self.evaluator = ExpressionEvaluator(self.context)

        # Validar sintaxis
        is_valid, errors = self.parser.validate_syntax(template)
        if not is_valid:
            raise SyntaxError(f"Template syntax errors: {'; '.join(errors)}")

        # Renderizar
        return self._render_recursive(template)

    def _render_recursive(self, template: str) -> str:
        """Renderizar template recursivamente."""
        result = []
        i = 0

        while i < len(template):
            # Buscar próxima expresión
            # Variables simples: {{variable}}
            var_match = re.search(r'\{\{([^#/}][^}]*?)\}\}', template[i:])

            # Bloques condicionales: {{#if}}
            if_match = re.search(r'\{\{#if\s+([^}]+)\}\}', template[i:])

            # Bloques for: {{#for}}
            for_match = re.search(r'\{\{#for\s+([^}]+)\}\}', template[i:])

            # Bloques switch: {{#switch}}
            switch_match = re.search(r'\{\{#switch\s+([^}]+)\}\}', template[i:])

            # Encontrar el match más cercano
            matches = []
            if var_match:
                matches.append(('var', var_match.start(), var_match))
            if if_match:
                matches.append(('if', if_match.start(), if_match))
            if for_match:
                matches.append(('for', for_match.start(), for_match))
            if switch_match:
                matches.append(('switch', switch_match.start(), switch_match))

            if not matches:
                # No hay más expresiones
                result.append(template[i:])
                break

            # Ordenar por posición
            matches.sort(key=lambda x: x[1])
            match_type, match_pos, match_obj = matches[0]

            # Agregar texto antes del match
            result.append(template[i:i + match_pos])

            # Procesar match
            if match_type == 'var':
                # Variable o función
                expr = match_obj.group(1).strip()
                value = self._evaluate_expression(expr)
                result.append(str(value))
                i += match_obj.end()

            elif match_type == 'if':
                # Bloque condicional
                condition = match_obj.group(1).strip()
                block_content, end_pos = self._extract_block(template[i:], 'if')
                rendered_block = self._render_if_block(condition, block_content)
                result.append(rendered_block)
                i += end_pos

            elif match_type == 'for':
                # Bloque for
                loop_expr = match_obj.group(1).strip()
                block_content, end_pos = self._extract_block(template[i:], 'for')
                rendered_block = self._render_for_block(loop_expr, block_content)
                result.append(rendered_block)
                i += end_pos

            elif match_type == 'switch':
                # Bloque switch
                switch_var = match_obj.group(1).strip()
                block_content, end_pos = self._extract_block(template[i:], 'switch')
                rendered_block = self._render_switch_block(switch_var, block_content)
                result.append(rendered_block)
                i += end_pos

        return ''.join(result)

    def _evaluate_expression(self, expr: str) -> Any:
        """Evaluar expresión (variable o función)."""
        # Función
        if '(' in expr:
            func_match = re.match(r'([^(]+)\((.*)\)', expr)
            if func_match:
                func_name = func_match.group(1).strip()
                args_str = func_match.group(2).strip()
                # Parsear argumentos
                args = []
                if args_str:
                    for arg in args_str.split(','):
                        arg = arg.strip()
                        # Evaluar cada argumento
                        args.append(self.evaluator._evaluate_value(arg))
                return self.functions.execute(func_name, *args)

        # Variable simple
        return self.evaluator._evaluate_value(expr)

    def _extract_block(self, template: str, block_type: str) -> tuple:
        """Extraer contenido de un bloque."""
        start_pattern = f'{{{{#{block_type}\\s+[^}}]+}}}}'
        end_pattern = f'{{{{/{block_type}}}}}'

        start_match = re.search(start_pattern, template)
        if not start_match:
            return '', 0

        level = 1
        pos = start_match.end()

        while pos < len(template) and level > 0:
            # Buscar próximo start o end
            next_start = re.search(start_pattern, template[pos:])
            next_end = re.search(end_pattern, template[pos:])

            if next_end is None:
                raise SyntaxError(f"Unclosed {block_type} block")

            if next_start and next_start.start() < next_end.start():
                level += 1
                pos += next_start.end()
            else:
                level -= 1
                if level == 0:
                    content = template[start_match.end():pos + next_end.start()]
                    return content, pos + next_end.end()
                pos += next_end.end()

        raise SyntaxError(f"Unclosed {block_type} block")

    def _render_if_block(self, condition: str, content: str) -> str:
        """Renderizar bloque if."""
        # Soportar else y elif
        parts = re.split(r'\{\{(else|elif\s+[^}]+)\}\}', content)

        # Evaluar condición principal
        if self.evaluator.evaluate(condition):
            return self._render_recursive(parts[0])

        # Evaluar elif y else
        i = 1
        while i < len(parts):
            if parts[i].strip() == 'else':
                return self._render_recursive(parts[i + 1])
            elif parts[i].strip().startswith('elif'):
                elif_condition = parts[i].strip()[4:].strip()
                if self.evaluator.evaluate(elif_condition):
                    return self._render_recursive(parts[i + 1])
            i += 2

        return ''

    def _render_for_block(self, loop_expr: str, content: str) -> str:
        """Renderizar bloque for."""
        variables, iterable = self.evaluator.evaluate_for_loop(loop_expr)
        result = []

        if len(variables) == 1:
            # Simple loop: for item in array
            var_name = variables[0]
            for item in iterable:
                # Crear contexto temporal
                old_value = self.context.get(var_name)
                self.context[var_name] = item
                self.evaluator = ExpressionEvaluator(self.context)

                # Renderizar contenido
                result.append(self._render_recursive(content))

                # Restaurar contexto
                if old_value is not None:
                    self.context[var_name] = old_value
                else:
                    self.context.pop(var_name, None)

        elif len(variables) == 2:
            # Loop con key, value: for key, value in object
            key_name, value_name = variables
            if isinstance(iterable, dict):
                items = iterable.items()
            else:
                items = enumerate(iterable)

            for key, value in items:
                old_key = self.context.get(key_name)
                old_value = self.context.get(value_name)

                self.context[key_name] = key
                self.context[value_name] = value
                self.evaluator = ExpressionEvaluator(self.context)

                result.append(self._render_recursive(content))

                # Restaurar
                if old_key is not None:
                    self.context[key_name] = old_key
                else:
                    self.context.pop(key_name, None)
                if old_value is not None:
                    self.context[value_name] = old_value
                else:
                    self.context.pop(value_name, None)

        return ''.join(result)

    def _render_switch_block(self, switch_var: str, content: str) -> str:
        """Renderizar bloque switch."""
        var_value = self.evaluator._evaluate_value(switch_var)

        # Extraer cases
        case_pattern = r'\{\{#case\s+([^}]+)\}\}(.*?)(?=\{\{#case|\{\{#default|\{\{/switch)'
        cases = re.finditer(case_pattern, content, re.DOTALL)

        for case_match in cases:
            case_value_str = case_match.group(1).strip()
            case_content = case_match.group(2)

            case_value = self.evaluator._evaluate_value(case_value_str)
            if var_value == case_value:
                return self._render_recursive(case_content)

        # Default case
        default_match = re.search(r'\{\{#default\}\}(.*?)$', content, re.DOTALL)
        if default_match:
            return self._render_recursive(default_match.group(1))

        return ''
