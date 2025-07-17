# services/exports.py
from typing import Iterable, Sequence, Callable, Any
import csv
from django.http import StreamingHttpResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from apps.devices.models import Bank, Branch, Device

# Column spec: (header_label, getter_function)
DEVICE_FIELDS = (
    ("branch_name".upper(), lambda d: d.branch.branch_name),
    ("serial_number".upper(), lambda d: d.serial_number),
    # ("bank_name", lambda d: d.branch.bank.name),
    ("created_at".upper(), lambda d: d.created_at.strftime("%Y-%m-%d")),  # Use your format_dt for consistency
    # ("updated_at", lambda d: d.updated_at.strftime("%Y-%m-%d")),
    ("notes".upper(), lambda d: d.notes or ""),
)


class _Echo:
    """Minimal write()-only buffer so csv.writer can stream rows."""
    def write(self, value: str) -> str:
        return value


def _iter_devices_csv_rows(qs: Iterable[Device], field_specs: Sequence[tuple[str, Callable[[Device], Any]]] = DEVICE_FIELDS, chunk_size: int = 1000):
    pseudo_buf = _Echo()
    writer = csv.writer(pseudo_buf)
    # Header
    yield writer.writerow([label for (label, _) in field_specs])
    # Data rows
    for d in qs.iterator(chunk_size=chunk_size):
        yield writer.writerow([getter(d) for (_, getter) in field_specs])


def export_branch_devices(branch_id: int, export_format: str = "csv") -> HttpResponse:
    """
    Stream an export of all Devices assigned to the specified Branch.
    """
    if export_format.lower() != "csv":
        raise ValueError("Unsupported export_format; only 'csv' is implemented.")

    # Validate branch exists
    try:
        branch = Branch.objects.select_related("bank").get(pk=branch_id)
    except ObjectDoesNotExist:
        return HttpResponse("Branch not found.", content_type="text/plain", status=404)

    qs = Device.objects.select_related("branch__bank").filter(branch_id=branch_id).order_by("serial_number")

    resp = StreamingHttpResponse(_iter_devices_csv_rows(qs), content_type="text/csv")
    
    # Dynamic filename as per your request
    bank_name = branch.bank.name.replace(" ", "_")  # Sanitize for safety
    branch_name = branch.branch_name.replace(" ", "_")
    fname = f"{bank_name}-{branch_name}.csv"
    resp["Content-Disposition"] = f'attachment; filename="{fname}"'
    
    return resp


def export_bank_devices(bank_id: int, export_format: str = "csv") -> HttpResponse:
    """
    Stream an export of all Devices assigned to all Branches of the specified Bank.
    (New function to complete your two-function suggestion.)
    """
    if export_format.lower() != "csv":
        raise ValueError("Unsupported export_format; only 'csv' is implemented.")

    # Validate bank exists
    try:
        bank = Bank.objects.get(pk=bank_id)
    except ObjectDoesNotExist:
        return HttpResponse("Bank not found.", content_type="text/plain", status=404)

    qs = Device.objects.select_related("branch__bank").filter(branch__bank_id=bank_id).order_by("branch__branch_name", "serial_number")

    resp = StreamingHttpResponse(_iter_devices_csv_rows(qs), content_type="text/csv")
    
    # Dynamic filename (using 'all' for aggregation)
    bank_name = bank.name.replace(" ", "_")
    fname = f"{bank_name}-all.csv"
    resp["Content-Disposition"] = f'attachment; filename="{fname}"'
    
    return resp