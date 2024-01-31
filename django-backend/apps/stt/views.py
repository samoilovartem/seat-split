import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from apps.stt.forms import DataProcessorForm
from apps.stt.services.process_raw_json_data import DataProcessor


@login_required
def process_file_view(request):
    if request.method == 'POST':
        form = DataProcessorForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = form.cleaned_data['json_file']
            season = form.cleaned_data['season']
            league = form.cleaned_data['league']
            replacements = form.cleaned_data.get('replacements')
            if replacements:
                dp = DataProcessor(json_file, 'output.csv', season, league, json.loads(replacements))
            else:
                dp = DataProcessor(json_file, 'output.csv', season, league)

            csv_content = dp.process_data()

            response = HttpResponse(csv_content, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="output.csv"'
            return response

    else:
        form = DataProcessorForm()

    return render(request, 'data_processing/json_to_processed_csv.html', {'form': form})
