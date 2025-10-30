"""
Template Functions - Funciones integradas para plantillas.

Proporciona funciones como DATE, MATH, STRING, FORMAT, RANDOM, USER.
"""

from datetime import datetime
from typing import Any, List
import random
import string
import uuid
import os


class TemplateFunctions:
    """Clase que proporciona todas las funciones disponibles en plantillas."""

    def __init__(self, context: dict = None):
        """
        Inicializar funciones con contexto.

        Args:
            context: Diccionario con información del contexto (usuario, proyecto, etc)
        """
        self.context = context or {}
        self._user_info = self.context.get('user', {})

    # ===== DATE Functions =====

    def date_now(self) -> str:
        """Retorna fecha y hora actual."""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def date_year(self) -> int:
        """Retorna año actual."""
        return datetime.now().year

    def date_month(self) -> int:
        """Retorna mes actual (1-12)."""
        return datetime.now().month

    def date_day(self) -> int:
        """Retorna día actual (1-31)."""
        return datetime.now().day

    def date_format(self, pattern: str) -> str:
        """
        Formatear fecha actual según patrón.

        Args:
            pattern: Patrón de formato (ej: 'DD/MM/YYYY', 'YYYY-MM-DD')
        """
        now = datetime.now()
        # Convertir pattern a formato Python
        py_pattern = pattern.replace('DD', '%d').replace('MM', '%m').replace('YYYY', '%Y')
        py_pattern = py_pattern.replace('HH', '%H').replace('mm', '%M').replace('ss', '%S')
        return now.strftime(py_pattern)

    # ===== MATH Functions =====

    def math_round(self, value: float, decimals: int = 0) -> float:
        """Redondear número."""
        return round(float(value), int(decimals))

    def math_sum(self, *values) -> float:
        """Sumar valores."""
        return sum(float(v) for v in values)

    def math_avg(self, *values) -> float:
        """Calcular promedio."""
        vals = [float(v) for v in values]
        return sum(vals) / len(vals) if vals else 0

    def math_percentage(self, value: float, total: float) -> float:
        """Calcular porcentaje."""
        return (float(value) / float(total) * 100) if float(total) != 0 else 0

    def math_min(self, *values) -> float:
        """Valor mínimo."""
        return min(float(v) for v in values)

    def math_max(self, *values) -> float:
        """Valor máximo."""
        return max(float(v) for v in values)

    # ===== STRING Functions =====

    def string_upper(self, text: str) -> str:
        """Convertir a mayúsculas."""
        return str(text).upper()

    def string_lower(self, text: str) -> str:
        """Convertir a minúsculas."""
        return str(text).lower()

    def string_capitalize(self, text: str) -> str:
        """Primera letra mayúscula."""
        return str(text).capitalize()

    def string_replace(self, text: str, find: str, replace: str) -> str:
        """Reemplazar texto."""
        return str(text).replace(str(find), str(replace))

    def string_trim(self, text: str) -> str:
        """Eliminar espacios al inicio y final."""
        return str(text).strip()

    def string_length(self, text: str) -> int:
        """Longitud del texto."""
        return len(str(text))

    # ===== FORMAT Functions =====

    def format_currency(self, amount: float, symbol: str = '$') -> str:
        """Formatear como moneda."""
        return f"{symbol}{float(amount):,.2f}"

    def format_number(self, value: float, decimals: int = 2) -> str:
        """Formatear número con separadores."""
        return f"{float(value):,.{int(decimals)}f}"

    def format_phone(self, number: str) -> str:
        """Formatear teléfono."""
        digits = ''.join(c for c in str(number) if c.isdigit())
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        return digits

    def format_percent(self, value: float) -> str:
        """Formatear como porcentaje."""
        return f"{float(value) * 100:.1f}%"

    # ===== RANDOM Functions =====

    def random_number(self, min_val: int, max_val: int) -> int:
        """Número aleatorio entre min y max."""
        return random.randint(int(min_val), int(max_val))

    def random_uuid(self) -> str:
        """UUID único."""
        return str(uuid.uuid4())

    def random_string(self, length: int) -> str:
        """String aleatorio."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=int(length)))

    # ===== USER Functions =====

    def user_name(self) -> str:
        """Nombre del usuario."""
        return self._user_info.get('name', os.getenv('USERNAME', 'Usuario'))

    def user_email(self) -> str:
        """Email del usuario."""
        return self._user_info.get('email', 'usuario@empresa.com')

    def user_date(self) -> str:
        """Fecha de creación."""
        return self.date_now()

    # ===== Método principal para ejecutar funciones =====

    def execute(self, function_name: str, *args) -> Any:
        """
        Ejecutar una función por nombre.

        Args:
            function_name: Nombre de la función (ej: 'DATE.now', 'MATH.round')
            *args: Argumentos de la función

        Returns:
            Resultado de la función
        """
        # Convertir 'DATE.now' a 'date_now'
        method_name = function_name.lower().replace('.', '_')

        # Buscar el método
        method = getattr(self, method_name, None)
        if method and callable(method):
            return method(*args)

        raise ValueError(f"Function '{function_name}' not found")

    def get_available_functions(self) -> List[str]:
        """Retorna lista de funciones disponibles."""
        return [
            name.replace('_', '.').upper()
            for name in dir(self)
            if not name.startswith('_') and callable(getattr(self, name))
            and name not in ['execute', 'get_available_functions']
        ]
