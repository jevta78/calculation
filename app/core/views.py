from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework import status
from .serializers import InputNumbersSerializer, SumCalcSerializer, AllSerializer
from rest_framework.response import Response
from .models import InputNumbers, Sums, Sve
from .utils import list_to_string


class InputNumView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = InputNumbers.objects.all()
    serializer_class = InputNumbersSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data['list_num'], int):
            serializer = InputNumbersSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user)
            return Response({"message": "Integer saved"}, status=status.HTTP_201_CREATED)
        else:
            lista_brojeva = [int(x) for x in data['list_num'].split(',') if x]
            for n in lista_brojeva:
                data={}
                data['list_num']=n
                serializer = InputNumbersSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=self.request.user)
            return Response({"message": "Integers saved"}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SumViewCalculate(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        zbir = InputNumbers.objects.filter(user=request.user)
        if not zbir.exists():
            return Response({"message": "There are no saved input numbers"}, status=status.HTTP_400_BAD_REQUEST)
        zbir = zbir.aggregate(Sum('list_num')).get('list_num__sum', 0)
        serializer = SumCalcSerializer(data={'calcSum':zbir})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response({"message":"Sum of numbers saved"}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SumViewList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Sums.objects.all()
    serializer_class = SumCalcSerializer

class AllView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, *args, **kwargs):

        numbers = list_to_string(InputNumbers.objects.all().values_list())
        sums = list_to_string(Sums.objects.all().values_list())

        data = {"numbers":numbers,
                "sums":sums}
        serializer = AllSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        InputNumbers.objects.filter(user=request.user).delete()
        Sums.objects.filter(user=request.user).delete()
        return Response({"message": "Data saved"},status=status.HTTP_201_CREATED)
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class History(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Sve.objects.all()
    serializer_class = AllSerializer

class HistoryDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Sve.objects.all()
    serializer_class = AllSerializer