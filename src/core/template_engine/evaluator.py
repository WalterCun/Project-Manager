"""
Expression Evaluator - Evalúa expresiones y condicionales.

Evalúa expresiones como:
- variable > 10
- name == "Juan"
- value1 && value2
"""

import re
from typing import Any, Dict


class ExpressionEvaluator:
    """Evaluador de expresiones para condicionales."""

    def __init__(self, context: Dict[str, Any]):
        """
        Inicializar evaluador.

        Args:
            context: Diccionario con variables disponibles
        """
        self.context = context

    def evaluate(self, expression: str) -> Any:
        """
        Evaluar una expresión.

        Args:
            expression: Expresión a evaluar

        Returns:
            Resultado de la expresión
        """
        expression = expression.strip()

        # Evaluar operadores lógicos
        if '&&' in expression or '||' in expression:
            return self._evaluate_logical(expression)

        # Evaluar comparaciones
        if any(op in expression for op in ['==', '!=', '>=', '<=', '>', '<']):
            return self._evaluate_comparison(expression)

        # Evaluar negación
        if expression.startswith('!'):
            return not self.evaluate(expression[1:])

        # Evaluar variable o valor literal
        return self._evaluate_value(expression)

    def _evaluate_logical(self, expression: str) -> bool:
        """Evaluar operador lógico (&&, ||)."""
        if '&&' in expression:
            parts = expression.split('&&')
            return all(self.evaluate(part.strip()) for part in parts)
        elif '||' in expression:
            parts = expression.split('||')
            return any(self.evaluate(part.strip()) for part in parts)
        return False

    def _evaluate_comparison(self, expression: str) -> bool:
        """Evaluar comparación (==, !=, >, <, >=, <=)."""
        operators = ['==', '!=', '>=', '<=', '>', '<']

        for op in operators:
            if op in expression:
                parts = expression.split(op, 1)
                if len(parts) == 2:
                    left = self._evaluate_value(parts[0].strip())
                    right = self._evaluate_value(parts[1].strip())

                    if op == '==':
                        return left == right
                    elif op == '!=':
                        return left != right
                    elif op == '>':
                        return left > right
                    elif op == '<':
                        return left < right
                    elif op == '>=':
                        return left >= right
                    elif op == '<=':
                        return left <= right

        return False

    def _evaluate_value(self, value: str) -> Any:
        """Evaluar un valor (variable, string, número, booleano)."""
        value = value.strip()

        # String literal
        if (value.startswith("'") and value.endswith("'")) or \
           (value.startswith('"') and value.endswith('"')):
            return value[1:-1]

        # Boolean
        if value.lower() == 'true':
            return True
        if value.lower() == 'false':
            return False

        # Number
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass

        # Variable del contexto
        if value in self.context:
            return self.context[value]

        # Si no se encuentra, retornar como string
        return value

    def evaluate_for_loop(self, expression: str) -> tuple:
        """
        Evaluar expresión de loop for.

        Soporta:
        - item in array
        - i in 1..10
        - key, value in object

        Args:
            expression: Expresión del for (ej: "item in array")

        Returns:
            Tupla (variable(s), iterable)
        """
        # Patrón: "var in iterable" o "key, value in iterable"
        match = re.match(r'(\w+(?:\s*,\s*\w+)?)\s+in\s+(.+)', expression)
        if not match:
            raise ValueError(f"Invalid for loop syntax: {expression}")

        vars_part = match.group(1).strip()
        iterable_part = match.group(2).strip()

        # Parsear variables
        variables = [v.strip() for v in vars_part.split(',')]

        # Evaluar iterable
        # Range: 1..10
        if '..' in iterable_part:
            range_match = re.match(r'(\d+)\.\.(\d+)', iterable_part)
            if range_match:
                start = int(range_match.group(1))
                end = int(range_match.group(2))
                iterable = list(range(start, end + 1))
            else:
                raise ValueError(f"Invalid range: {iterable_part}")
        # Variable del contexto
        elif iterable_part in self.context:
            iterable = self.context[iterable_part]
        else:
            raise ValueError(f"Variable '{iterable_part}' not found in context")

        return variables, iterable
