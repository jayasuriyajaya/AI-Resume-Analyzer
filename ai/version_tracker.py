def get_next_version(
    connection,
    user_id
):
    """
    Return the next resume version number
    for a specific user.
    """

    result = connection.execute(
        """
        SELECT MAX(version_number)
        FROM resume_versions
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()


    current_version = result[0]


    if current_version is None:

        return 1


    return current_version + 1