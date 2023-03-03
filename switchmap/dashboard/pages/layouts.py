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
    )
    result = result.replace(
        "<thead><tr><th></th><th></th><th></th><th></th></tr></thead>", ""
    ).strip()
    return result
