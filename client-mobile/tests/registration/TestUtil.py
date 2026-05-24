import subprocess


def run_database_seed():
    """Runs the database seeding script inside the running Docker container."""
    print("Initiating database seeding inside Docker container...")

    # We remove the '-i' flag so it runs cleanly in a non-interactive automation window
    command = ["docker", "compose", "exec", "-t", "api-server", "npm", "run", "seed"]

    try:
        # Run the command and capture output so it shows cleanly in PyCharm's console
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        print("Docker Output:\n", result.stdout)
        print("Database seeding completed successfully!")

    except subprocess.CalledProcessError as e:
        print("\nFailed to run database seed inside Docker container!")
        print("Error Output:\n", e.stderr)
        # Raise the error so the Selenium test halts before trying to interact with an empty DB
        raise e