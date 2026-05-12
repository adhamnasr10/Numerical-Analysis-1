from __future__ import annotations
import customtkinter as ctk
from ui._base_page import BasePage, BG_MAIN, BG_CARD, ACCENT, ACCENT2, TEXT_PRI, TEXT_SEC
from methods.euler import euler, modified_euler
from graphs.differential_graphs import plot_euler
from utils.parser import parse_ode
from utils.validators import validate_float


class DifferentialPage(BasePage):
    def __init__(self,parent,**kwargs): super().__init__(parent,**kwargs); self._c1=None; self._build()
    def _build(self):
        ctk.CTkLabel(self,text="📈  Differential Equations",text_color=ACCENT,font=ctk.CTkFont(size=22,weight="bold")).pack(anchor="w",padx=20,pady=(18,2))
        self._method=ctk.StringVar(value="Euler"); tab=ctk.CTkFrame(self,fg_color="transparent"); tab.pack(anchor="w",padx=20)
        for m in ["Euler","Modified Euler"]: ctk.CTkRadioButton(tab,text=m,variable=self._method,value=m,text_color=TEXT_PRI,fg_color=ACCENT).pack(side="left",padx=10)
        content=ctk.CTkFrame(self,fg_color="transparent"); content.pack(fill="both",expand=True,padx=20,pady=8); content.columnconfigure(1,weight=1)
        inp=ctk.CTkFrame(content,fg_color=BG_CARD,corner_radius=12,width=260); inp.grid(row=0,column=0,sticky="ns",padx=(0,12)); inp.grid_propagate(False)
        ctk.CTkLabel(inp,text="Parameters",text_color=ACCENT2,font=ctk.CTkFont(size=14,weight="bold")).pack(anchor="w",padx=14,pady=(14,8))
        for attr,label,default in [("_e_fn","f(x,y)","x + y"),("_e_x0","x0","0"),("_e_y0","y0","1"),("_e_h","h","0.1"),("_e_xe","x end","1.0")]:
            fr,en=self.labeled_entry(inp,label,default,width=220); fr.pack(padx=14,pady=4,fill="x"); setattr(self,attr,en)
        ctk.CTkButton(inp,text="  ▶  Solve ODE",height=38,fg_color=ACCENT,text_color="#000000",command=self._solve).pack(padx=14,pady=(16,6),fill="x")
        out=ctk.CTkScrollableFrame(content,fg_color=BG_MAIN); out.grid(row=0,column=1,sticky="nsew"); self._result_lbl=self.make_result_label(out); self._gf=ctk.CTkFrame(out,fg_color=BG_CARD,height=300); self._gf.pack(fill="x",pady=4); self._tbl_card=ctk.CTkFrame(out,fg_color=BG_CARD); self._tbl_card.pack(fill="x",pady=4)
    def _embed(self,fig):
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        if self._c1: self._c1.get_tk_widget().destroy()
        for w in self._gf.winfo_children(): w.destroy()
        c=FigureCanvasTkAgg(fig,master=self._gf); c.draw(); c.get_tk_widget().pack(fill="both",expand=True); self._c1=c
    def _solve(self):
        try:
            f=parse_ode(self._e_fn.get()); x0=validate_float(self._e_x0.get(),"x0"); y0=validate_float(self._e_y0.get(),"y0"); h=validate_float(self._e_h.get(),"h"); xe=validate_float(self._e_xe.get(),"x end"); method=self._method.get(); xs,ys,table=(euler(f,x0,y0,h,xe) if method=="Euler" else modified_euler(f,x0,y0,h,xe)); self._embed(plot_euler(xs,ys,method)); self.show_table(self._tbl_card,table); self.show_result(self._result_lbl,f"OK  y({xs[-1]:.4f}) ≈ {ys[-1]:.8f} | Method: {method}")
        except Exception as ex: self.show_result(self._result_lbl,f"Error: {ex}",error=True)
