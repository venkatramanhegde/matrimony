from rest_framework import serializers
from .models import User, UserDetails


class LoginSerializer(serializers.Serializer):
    """This is the serializer used for logging in user"""
    phone_no = serializers.CharField(max_length=25, required=True)
    password = serializers.CharField(
        style={'input_type': 'password'},  write_only=True, required=True
    )

    class Meta:
        model = User
        fields = ('phone_no', 'password')


class SignUpSerializer(serializers.Serializer):
    """This is the serializer used for signup in user"""
    first_name = serializers.CharField(max_length=60, allow_blank=False)
    father_name = serializers.CharField(max_length=60, allow_blank=True)
    phone_no = serializers.CharField(max_length=25, allow_blank=True)
    password = serializers.CharField(max_length=256, allow_blank=False)
    is_admin = serializers.BooleanField()
    is_user = serializers.BooleanField()
    is_male = serializers.BooleanField()
    is_female = serializers.BooleanField()
    gender = serializers.CharField(max_length=10)
    email = serializers.EmailField(max_length=100, allow_blank=True)
    date_of_birth = serializers.DateField()
    # age = serializers.IntegerField()
    height = serializers.FloatField()
    weight = serializers.FloatField()
    gotra = serializers.CharField(max_length=50, allow_blank=True)
    community = serializers.CharField(max_length=50, allow_blank=True)
    caste = serializers.CharField(max_length=50, allow_blank=True)
    occupation = serializers.CharField(max_length=100, allow_blank=True)
    photo1 = serializers.FileField(allow_null=True)
    horoscope = serializers.FileField(allow_null=True)


    class Meta:
        model = User, UserDetails

    def create(self, validated_data):
        user = User.objects.create(first_name=validated_data.get("first_name"),
                                   father_name=validated_data.get("father_name"),
                                   phone_no=validated_data.get("phone_no"),
                                   is_admin=validated_data.get("is_admin"),
                                   is_user=validated_data.get("is_user"),
                                   is_male=validated_data.get("is_male"),
                                   is_female=validated_data.get("is_female"),
                                   gender=validated_data.get("gender"),
                                   date_of_birth=validated_data.get("date_of_birth"),
                                   email=validated_data.get("email"),

                                   )
        user.set_password(validated_data.get("password"))
        user_detail=UserDetails.objects.create(**validated_data, user_id=user.id,
                                               # father_name=validated_data.get("father_name"),
                                               # phone_no=validated_data.get("phone_no"),
                                               # is_male=validated_data.get("is_male"),
                                               # is_female=validated_data.get("is_female"),
                                               # gender=validated_data.get("gender"),
                                               # height=validated_data.get("height"),
                                               # weight=validated_data.get("weight"),
                                               # gotra=validated_data.get("gotra"),
                                               # community=validated_data.get("community"),
                                               # caste=validated_data.get("caste"),
                                               # occupation=validated_data.get("occupation"),
                                               # date_of_birth=validated_data.get("date_of_birth"),

                                               )
        # user_detail = UserDetails.objects.create(user_id=user.id,
        #                                          first_name=validated_data.get("first_name"),
        #                                          father_name=validated_data.get("father_name"),
        #                                          phone_no=validated_data.get("phone_no"),
        #                                          # is_admin=validated_data.get("is_admin"),
        #                                          # is_user=validated_data.get("is_user"),
        #                                          is_male=validated_data.get("is_male"),
        #                                          is_female=validated_data.get("is_female"),
        #                                          gender=validated_data.get("gender"),
        #                                          )
        # add_user.user = user.id
        print(user.id)
        user_detail.save()
        user.save()
        return user


class AdminPageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    first_name = serializers.CharField()
    father_name = serializers.CharField()
    phone_no = serializers.CharField()
    gender = serializers.CharField()
    # email = serializers.EmailField()
    date_of_birth = serializers.DateField()
    # is_approved = serializers.BooleanField()
    height = serializers.FloatField()
    weight = serializers.FloatField()
    community = serializers.CharField(max_length=50, allow_blank=True)
    caste = serializers.CharField(max_length=50, allow_blank=True)
    occupation = serializers.CharField(max_length=100, allow_blank=True)
    age = serializers.IntegerField()


    class Meta:
        model = UserDetails
        fields = ('id', 'user_id', 'first_name', 'father_name', 'phone_no', 'gender',  'date_of_birth',
                  'height', 'weight')




class UpdateUserSerializer(serializers.Serializer):
    """This is the serializer used for signup in user"""
    hav_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=60, allow_blank=False)
    last_name = serializers.CharField(max_length=50, allow_blank=True)
    phone_no = serializers.CharField(max_length=25, allow_blank=True)
    # is_male = serializers.BooleanField()
    # is_female = serializers.BooleanField()
    # is_approved = serializers.BooleanField(default=False)
    # gender = serializers.CharField(max_length=10)
    age = serializers.IntegerField()
    father_name = serializers.CharField(max_length=60, allow_blank=True)
    mother_name = serializers.CharField(max_length=60, allow_blank=True)
    address = serializers.CharField(max_length=250, allow_blank=True)
    community = serializers.CharField(max_length=50, allow_blank=True)
    caste = serializers.CharField(max_length=50, allow_blank=True)
    gotra = serializers.CharField(max_length=50, allow_blank=True)
    nakshatra = serializers.CharField(max_length=50, allow_blank=True)
    rashi = serializers.CharField(max_length=50, allow_blank=True)
    material_status = serializers.CharField(max_length=50, allow_blank=True)
    height = serializers.FloatField()
    weight = serializers.FloatField()
    job_position = serializers.CharField(max_length=100, allow_blank=True)
    highest_education = serializers.CharField(max_length=100, allow_blank=True)
    company_name = serializers.CharField(max_length=100, allow_blank=True)
    occupation = serializers.CharField(max_length=100, allow_blank=True)
    date_of_birth = serializers.DateField()
    mother_tongue = serializers.CharField(max_length=50, allow_blank=True)
    class Meta:
        model = User

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.age = validated_data.get('age', instance.age)
        instance.father_name = validated_data.get('father_name', instance.father_name)
        instance.mother_name = validated_data.get('mother_name', instance.mother_name)
        instance.address = validated_data.get('address', instance.address)
        instance.community = validated_data.get('community', instance.community)
        instance.caste = validated_data.get('caste', instance.caste)
        instance.gotra = validated_data.get('gotra', instance.gotra)
        instance.nakshatra = validated_data.get('nakshatra', instance.nakshatra)
        instance.rashi = validated_data.get('rashi', instance.rashi)
        instance.material_status = validated_data.get('material_status', instance.material_status)
        instance.height = validated_data.get('height', instance.height)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.job_position = validated_data.get('job_position', instance.job_position)
        instance.highest_education = validated_data.get('highest_education', instance.highest_education)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.occupation = validated_data.get('occupation', instance.occupation)
        instance.mother_tongue = validated_data.get('mother_tongue', instance.mother_tongue)


        return instance

    # hav_id = serializers.IntegerField()
        # first_name = serializers.CharField(max_length=60, allow_blank=False)
        # last_name = serializers.CharField(max_length=50, allow_blank=True)
        # phone_no = serializers.CharField(max_length=25, allow_blank=True)
        # is_male = serializers.BooleanField()
        # is_female = serializers.BooleanField()
        # is_approved = serializers.BooleanField(default=False)
        # gender = serializers.CharField(max_length=10)
        # age = serializers.IntegerField()
        # father_name = serializers.CharField(max_length=60, allow_blank=True)
        # mother_name = serializers.CharField(max_length=60, allow_blank=True)
        # address = serializers.CharField(max_length=250, allow_blank=True)
        # community = serializers.CharField(max_length=50, allow_blank=True)
        # caste = serializers.CharField(max_length=50, allow_blank=True)
        # gotra = serializers.CharField(max_length=50, allow_blank=True)
        # nakshatra = serializers.CharField(max_length=50, allow_blank=True)
        # rashi = serializers.CharField(max_length=50, allow_blank=True)
        # material_status = serializers.CharField(max_length=50, allow_blank=True)
        # height = serializers.FloatField()
        # weight = serializers.FloatField()
        # job_position = serializers.CharField(max_length=100, allow_blank=True)
        # highest_education = serializers.CharField(max_length=100, allow_blank=True)
        # date_of_birth = serializers.DateField()
        # mother_tongue = serializers.CharField(max_length=50, allow_blank=True)


class UserPageSerializer(serializers.Serializer):
    pass


class UserDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    hav_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=60, allow_blank=False)
    last_name = serializers.CharField(max_length=50, allow_blank=True)
    phone_no = serializers.CharField(max_length=25, allow_blank=True)
    is_male = serializers.BooleanField()
    is_female = serializers.BooleanField()
    is_approved = serializers.BooleanField(default=False)
    is_reject = serializers.BooleanField(default=False)
    gender = serializers.CharField(max_length=10)
    age = serializers.IntegerField()
    father_name = serializers.CharField(max_length=60, allow_blank=True)
    mother_name = serializers.CharField(max_length=60, allow_blank=True)
    address = serializers.CharField(max_length=250, allow_blank=True)
    community = serializers.CharField(max_length=50, allow_blank=True)
    caste = serializers.CharField(max_length=50, allow_blank=True)
    gotra = serializers.CharField(max_length=50, allow_blank=True)
    nakshatra = serializers.CharField(max_length=50, allow_blank=True)
    rashi = serializers.CharField(max_length=50, allow_blank=True)
    material_status = serializers.CharField(max_length=50, allow_blank=True)
    height = serializers.FloatField()
    weight = serializers.FloatField()
    job_position = serializers.CharField(max_length=100, allow_blank=True)
    highest_education = serializers.CharField(max_length=100, allow_blank=True)
    company_name = serializers.CharField(max_length=100, allow_blank=True)
    occupation = serializers.CharField(max_length=100, allow_blank=True)
    date_of_birth = serializers.DateField()
    mother_tongue = serializers.CharField(max_length=50, allow_blank=True)


    class Meta:
        model = UserDetails
        # fields = ('id', 'user_id', 'hav_id', 'age', 'height', 'community', 'caste',
        #           'highest_education', 'is_approved', 'photo1', 'horoscope')
        fields = ('__all__')


class LogedinUserDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    first_name = serializers.CharField()
    father_name = serializers.CharField()
    phone_no = serializers.CharField()
    gender = serializers.CharField()
    # email = serializers.EmailField()
    date_of_birth = serializers.DateField()
    # is_approved = serializers.BooleanField()
    is_admin = serializers.BooleanField()
    height = serializers.FloatField()
    weight = serializers.FloatField()
    community = serializers.CharField(max_length=50, allow_blank=True)
    caste = serializers.CharField(max_length=50, allow_blank=True)
    occupation = serializers.CharField(max_length=100, allow_blank=True)
    age = serializers.IntegerField()

    class Meta:
        model = UserDetails
        fields = ('id', 'user_id', 'first_name', 'father_name', 'phone_no', 'gender', 'date_of_birth',
                  'height', 'weight', 'is_admin')