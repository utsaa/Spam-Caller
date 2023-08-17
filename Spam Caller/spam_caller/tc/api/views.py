from django.contrib.auth.models import User

from rest_framework.filters import SearchFilter
from .serializers import PhoneSerializer, PhoneSerializerReg
from tc.models import Phone

from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class PhoneViewSet(ListAPIView):
    queryset= Phone.objects.all()
    
    serializer_class= PhoneSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_fields=['phone','user__username']
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticated]


    def get_inc(self, in_contact):
        return Phone.objects.filter(id__in=in_contact)

    def get_outc(self, out_contact):
        return Phone.objects.filter(id__in=out_contact)
            
    def list(self,request):

        phone=self.request.query_params.get('phone')
        username=self.request.query_params.get('user__username',None)

        # if self.request.user.is_authenticated:
        #     self.serializer_class=PhoneSerializerReg
        
        
        if phone:
            # If the phone is in the registered user that phone object is selected
            ph=self.serializer_class(Phone.objects.filter(phone__iexact=phone, user__in=User.objects.all()), many=True)
            print('here in ph',ph.data)
            if not ph:
                # If the phone user is not registered the phone user matches is selected
                ph=self.serializer_class(Phone.objects.filter(phone__iexact=phone), many=True)
            
            if ph: return Response(ph.data)
            
        else:
            ph=Phone.objects.none()
        
        if username:
            # First look for the username that exactly matches
            uname1=Phone.objects.filter(user__username__iexact=username).annotate(qs_order=models.Value(0, models.IntegerField()))
            # Then look for the username that initiates with the query
            uname2=Phone.objects.filter(user__username__startswith=username).annotate(qs_order=models.Value(1, models.IntegerField()))
            # Then the username that contains the query
            uname3=Phone.objects.filter(user__username__icontains=username).annotate(qs_order=models.Value(2, models.IntegerField()))
            
            uname=uname1.union(uname2,uname3)
            uname=uname.order_by('qs_order')
            # print('uname is there',uname)
        else:
            uname=Phone.objects.none()
           
        
        if ph or uname:
            ph=ph.union(uname)
            ph=self.serializer_class(ph,many=True)
            seen=set()
            new_ph=[]
            for p in ph.data:
                # This eliminates all the duplicate value in search
                if p['id'] not in seen: 
                    seen.add(p['id'])
                    new_ph.append(p)
            return Response(new_ph)
        else:
            if not self.request.user.is_authenticated:
                # If user is not authenticated all the values are returned
                ph=Phone.objects.all()
                ph=self.serializer_class(ph,many=True)
                return Response(ph.data)

            else:
                # Here, the contacts in the contact list and not in the contact list is returned
                phones=Phone.objects.all()
                in_contact=[];out_contact=[]
                contacts=Phone.objects.filter(contact_list__in=[self.request.user])
                for contact in contacts:
                    if User.objects.filter(id=contact.user.id):
                            in_contact.append(contact.id)
                for phone in phones:
                    if phone.id not in in_contact: 
                        out_contact.append(phone.id)

                print('The incontact values', in_contact)
                print('The outcontact values', out_contact)
                # The contact list data would show the email id and others wonts
                self.serializer_class=PhoneSerializer
                ph2=self.serializer_class(self.get_outc(in_contact), many=True)
                self.serializer_class=PhoneSerializerReg
                ph1=self.serializer_class(self.get_inc(out_contact),many=True)
                

                
                

                # self.serializer_class=PhoneSerializer
                # ph2=Phone.objects.filter(id__in=out_contact)
                print('ph1',ph1.data, 'ph2',ph2.data)

                return Response({'in_contact': ph1.data, 'out_contact': ph2.data})

    
        

    