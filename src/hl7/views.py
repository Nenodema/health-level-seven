from django.http import HttpResponse
from django.shortcuts import render
from .forms import TextInputForm
from src.converter import data_to_hl7, convert, hl7_to_csv, hl7_to_excel


def home_view(request):
    return render(request,
                  "home.html")


def textbox_view(request):
    return render(request,
                  'upload.html')


def upload_csv(request):
    return render(request,
                  'csv_to_hl7.html')


def upload_excel(request):
    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            if csv_file.name.endswith('.csv'):
                data = csv_file.read().decode('utf-8')
                hl7_message = data_to_hl7(
                    hl7_data=convert(data)
                )
                return render(request,
                              'excel_to_hl7.html',
                              {'hl7_message': hl7_message})
            else:
                return render(request,
                              'excel_to_hl7.html',
                              {'error_message': 'Invalid file format. Please upload a Excel file.'})
        else:
            return render(request,
                          'excel_to_hl7.html',
                          {'error_message': 'No file uploaded. Please select a Excel file to upload.'})
    return render(request,
                  'excel_to_hl7.html')


def text_input(request):
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            submitted_text = form.cleaned_data['text_input']
            try:
                hl7_message = data_to_hl7(
                    hl7_data=convert(submitted_text)
                )
            except:
                return render(request,
                              'text_to_hl7.html',
                              {'error_message': 'Please enter text in the required csv format'})
            return render(request,
                          'text_to_hl7.html',
                          {'hl7_message': hl7_message})
        else:
            return render(request,
                          'text_to_hl7.html',
                          {'error_message': 'No text submitted'})
    else:
        form = TextInputForm()

    return render(request,
                  'text_to_hl7.html',
                  {'form': form})


def hl7_to_csv(request):
    if request.method == 'POST':

        form = TextInputForm(request.POST)
        if form.is_valid():
            submitted_text = form.cleaned_data['text_input']
            if '|' not in submitted_text:
                return render(request,
                              'hl7_to_csv.html',
                              {'error_message': 'Please upload the required HL7 format'})
            try:
                csv_data = hl7_to_csv(submitted_text)  # Transform HL7 to CSV-like format
            except:
                pass

            else:
                context = {
                    'csv_data': csv_data,  # Use the transformed CSV data
                }
                return render(request, 'hl7_to_csv.html', context)
        else:
            return render(request,
                          'hl7_to_csv.html',
                          {'error_message': 'No HL7 message submitted'})

    form = TextInputForm()
    context = {
        'form': form,
    }
    return render(request, 'hl7_to_csv.html', context)


def hl7_to_excel(request):
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            submitted_text = form.cleaned_data['text_input']
            if '|' not in submitted_text:
                return render(
                    request,
                    'hl7_to_excel.html',
                    {'error_message': 'Please upload the required HL7 format'}
                )
            try:
                excel_data = hl7_to_excel(submitted_text)  # Transform HL7 to Excel format
                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; filename="converted_data.xlsx"'
                response.write(excel_data)
                return response
            except Exception as e:
                return render(
                    request,
                    'hl7_to_excel.html',
                    {'error_message': 'An error occurred during conversion'}
                )
        else:
            return render(
                request,
                'hl7_to_excel.html',
                {'error_message': 'No HL7 message submitted'}
            )

    form = TextInputForm()
    context = {'form': form}
    return render(request,
                  'hl7_to_excel.html', context)
