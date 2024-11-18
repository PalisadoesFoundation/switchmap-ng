"""Module of page layout functions."""


def table_wrapper(title, table, strip=True):
    """Wrap the data in HTML stuff.

    Args:
        title: title
        table: Table HTML
        strip: Strip the thead if True

    Returns:
        result: HTML

    """
    # Initialize key variables
    #
    result = f"""
    <div class="row">
      <div class="col-lg-12">
          <div class="panel panel-default">
              <div class="panel-heading">
                {title}
              </div>
              <!-- /.panel-heading -->
              <div class="panel-body">
                {table}
              </div>
              <!-- /.panel-body -->
          </div>
          <!-- /.panel -->
      </div>
    </div>
""".strip()

    if bool(strip) is True:
        result = remove_thead(result)
    return result


def remove_thead(data):
    """Remove line in HTML code containing the 'thead'.

    Args:
        data: HTML code

    Returns:
        result: HTML

    """
    # Initialize key variables
    fixed = []

    # Process
    lines = data.split("\n")
    for line in lines:
        if "thead" in line.lower():
            continue
        fixed.append(line)

    # Return
    result = "\n".join(fixed)
    return result
