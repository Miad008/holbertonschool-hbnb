from app.core.models.base import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def to_dict(self):
        """يرجع بيانات المستخدم كقاموس متسق مع JSON"""
        base_dict = super().to_dict()
        base_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        })
        return base_dict

#class User:
 #   def __init__(self, first_name, last_name, email, id=None):
  #      self.id = id  # ممكن يجي من الخارج أو يتم توليده داخل التخزين
   #     self.first_name = first_name
    #    self.last_name = last_name
     #   self.email = email

#    def to_dict(self):
#        """يرجع البيانات كقاموس (JSON ready)"""
 #       return {
  #          "id": self.id,
   #         "first_name": self.first_name,
    #        "last_name": self.last_name,
     #       "email": self.email
      #  }
