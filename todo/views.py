import time
from django.core.paginator import Paginator
from django.core.cache import cache
from django.shortcuts import render,redirect
from .models import ToDo
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import csv

def todo_list(request):
    start_time = time.time()  # Start time tracking

    todo = ToDo.objects.all()  # Non-optimized query
    fetch_time = time.time() - start_time  # Calculate fetching time

    print(f"Fetching time (Non-Optimized with Execution): {fetch_time:.4f} seconds")

    return render(request, 'todo/todo_list.html', {'todo': todo, 'fetch_time': fetch_time})


def todo_list1(request):
    start_time = time.time()  # Start time tracking

    # Check if data is cached
    todo1 = cache.get("todo_list")
    if not todo1:
        todo1 = list(ToDo.objects.only("title", "completed").order_by("-created_at"))  # Optimized Query
        cache.set("todo_list", todo1, timeout=300)  # Cache for 5 minutes

    fetch_time = time.time() - start_time  # Calculate fetching time

    # Pagination: Show 10 items per page
    paginator = Paginator(todo1, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    print(f"Fetching time (Optimized with Cache & Pagination): {fetch_time:.4f} seconds")  # Print in console

    return render(request, 'todo/todo_list1.html', {'page_obj': page_obj, 'fetch_time': fetch_time})


def import_todo(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        # Check if the uploaded file is a CSV
        if not csv_file.name.endswith(".csv"):
            messages.error(request, "Invalid file format. Please upload a CSV file.")
            return redirect("import_todo")

        # Read and process the CSV file
        try:
            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.reader(decoded_file)
            next(reader)  # Skip header row

            todo_list = []
            for row in reader:
                if len(row) >= 3:  # Ensure at least 3 columns (title, description, completed)
                    title, description, completed = row[0], row[1], row[2].strip().lower() in ["true", "1", "yes"]
                    todo_list.append(ToDo(title=title, description=description, completed=completed))

            # Bulk create to improve performance
            ToDo.objects.bulk_create(todo_list)
            messages.success(request, f"Successfully imported {len(todo_list)} ToDo items.")
        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")

        return redirect("import_todo")

    return render(request, "todo/import_todo.html")
