def show_changed_fields(obj, fields):
    delta = obj.diff_against(obj.prev_record)

    for change in delta.changes:
        fields += str(
            f'<strong>{change.field}</strong> changed from <span style="background-color:#E4260C">{change.old}'
            f'</span> to <span style="background-color:#92BF0F">{change.new}</span> . <br/>'
        )
    return fields
