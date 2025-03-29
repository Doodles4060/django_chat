from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from time import perf_counter

from .forms import SVGPixelationForm
from .svg_pixelator import SVGPixelator

class SVGPixelationView(View):
    template_name = 'tools/pixelation.html'

    def get(self, request):
        return render(request, self.template_name, context={'form': SVGPixelationForm})

    def post(self, request):
        form = SVGPixelationForm(request.POST, request.FILES)

        if form.is_valid():
            svg_file = form.cleaned_data['svg_file']
            aspect_ratio = form.cleaned_data['aspect_ratio']
            pixelation_level = form.cleaned_data['pixelation_level']

            try:
                pixelator = SVGPixelator(svg_file, aspect_ratio, pixelation_level)

                time_start = perf_counter()
                image_base64 = pixelator.get_final_image_base64()
                time_stop = perf_counter()
                messages.success(request, f'Image pixelation took {time_stop - time_start:.2f} seconds!')
                messages.info(request, f'Image size: {len(image_base64) / 1024**2:.2f}mb')
            except ValueError as e:
                messages.error(request, str(e))
                return render(request, self.template_name, context={'form': form})

            context = {
                'form': SVGPixelationForm(),
                'image_base64': image_base64
            }
            return render(request, self.template_name, context)

        messages.error(request, 'Failed to upload the file!')
        return render(request, self.template_name, context={'form': SVGPixelationForm})
