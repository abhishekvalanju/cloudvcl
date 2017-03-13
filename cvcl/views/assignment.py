from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.views import View
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.db import transaction
from django.db.models import Q
import yaml, base64
from passlib.hash import sha512_crypt
from ..models import *
from ..forms import AssignmentForm
from ..osapi import get_default_network_id, os_connect


def is_instructor_check(user):
    return user.is_instructor


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class AssignmentCreate(LoginRequiredMixin, CreateView):
    template_name = './assignment_create.html'
    form_class = AssignmentForm

    def get_form_kwargs(self):
        kwargs = super(AssignmentCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        return super(AssignmentCreate, self).form_valid(form)


class AssignmentDetail(LoginRequiredMixin, DetailView):
    template_name = './assignment_detail.html'

    def get_queryset(self):
        return Assignment.objects.filter(Q(course__in=self.request.user.instructs.all()) | Q(
            course__in=self.request.user.studies.all(), start_date__lte=timezone.now(),
            end_date__gte=timezone.now())).distinct()

    def get_context_data(self, **kwargs):
        context = super(AssignmentDetail, self).get_context_data(**kwargs)
        try:
            context['environment'] = self.object.environments.get(user=self.request.user)
        except Environment.DoesNotExist:
            pass
        return context


class AssignmentList(LoginRequiredMixin, ListView):
    template_name = './assignment_list.html'

    def get_queryset(self):
        return Assignment.objects.filter(Q(course__in=self.request.user.instructs.all()) | Q(
            course__in=self.request.user.studies.all(), start_date__lte=timezone.now(),
            end_date__gte=timezone.now())).distinct()


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class AssignmentUpdate(LoginRequiredMixin, UpdateView):
    template_name = './assignment_update.html'
    form_class = AssignmentForm

    def get_form_kwargs(self):
        kwargs = super(AssignmentUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Assignment.objects.filter(course__in=self.request.user.instructs.all())


@method_decorator(user_passes_test(is_instructor_check), name='dispatch')
class AssignmentDelete(LoginRequiredMixin, DeleteView):
    template_name = './assignment_delete.html'
    success_url = reverse_lazy('assignments')

    def get_queryset(self):
        return Assignment.objects.filter(course__in=self.request.user.instructs.all())


@method_decorator(transaction.atomic, name='dispatch')
class AssignmentLaunch(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        assignment = get_object_or_404(Assignment, pk=kwargs['pk'])
        if assignment.course.instructor != request.user:
            if assignment.start_date > timezone.now() or assignment.end_date < timezone.now():
                # student's can't launch environment outside specified dates
                return HttpResponseForbidden()
        else:
            if assignment.end_date < timezone.now():
                # instructors can't launch environment after assignment expired (it would get cleaned up soon)
                return HttpResponseForbidden()

        if request.user not in assignment.course.students.all():
            # student not in course/assignment
            return HttpResponseForbidden()

        if assignment.environments.filter(user=request.user):
            # already exists
            return HttpResponseForbidden()

        environment = Environment(assignment=assignment, user=request.user)
        environment.save()

        for vmd in environment.assignment.environment_definition.vmdefinition_set.all():
            os_conn = os_connect()
            username = self.request.user.username
            password = get_random_string(length=8)
            user_data = '#cloud-config\n' + yaml.dump({
                # 'password': password,
                'users': [
                    'default',
                    {
                        'name': username,
                        'sudo': 'ALL = (ALL) NOPASSWD: ALL',
                        'lock_passwd': False,
                        'passwd': sha512_crypt.encrypt(password),
                    }
                ],
            }, default_flow_style=False)
            server = os_conn.compute.create_server(
                name=vmd.name + '.' + username,
                image_id=vmd.image.uuid,
                flavor_id=vmd.flavor.uuid,
                networks=[{"uuid": get_default_network_id()}],
                user_data=base64.b64encode(bytes(user_data, 'utf-8')).decode('utf-8')
            )

            vm = environment.vms.create(
                name=server.name,
                uuid=server.id,
                status=server.status,
                ip_address=server.access_ipv4,
                vm_definition=vmd,
                username=username,
                password=password,
            )
            server = os_conn.compute.wait_for_server(server)
            # print(server)
            server = os_conn.compute.get_server(server.id)
            # print(server)
            vm.status = server.status
            vm.ip_address = server.addresses[list(server.addresses.keys())[0]][0]['addr']
            vm.save()

        return redirect(environment)