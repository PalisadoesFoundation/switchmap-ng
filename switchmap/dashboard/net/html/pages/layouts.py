"""Module of page layout functions."""


def table_wrapper(title, table):
    """Wrap the data in HTML stuff.

    Args:
        title: title
        table: Table HTML

    Returns:
        result: HTML

    """
    # Initialize key variables
    result = """
    <div class="row">
      <div class="col-lg-12">
          <div class="panel panel-default">
              <div class="panel-heading">
                  {}
              </div>
              <!-- /.panel-heading -->
              <div class="panel-body">
                  <div class="table-responsive table-bordered">
                      {}
                  </div>
                  <!-- /.table-responsive -->
              </div>
              <!-- /.panel-body -->
          </div>
          <!-- /.panel -->
      </div>
    </div>
""".format(
        title, table
    ).strip()
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
