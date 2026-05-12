from __future__ import annotations
import customtkinter as ctk
import sympy as sp
from ui._base_page import BasePage, BG_MAIN, BG_CARD, ACCENT, ACCENT2, TEXT_PRI, TEXT_SEC
from methods.trapezoidal import trapezoidal
from methods.simpson import simpson_one_third, simpson_three_eighth
from graphs.integration_graphs import plot_integration
from utils.parser import parse_function, get_sympy_expr
from utils.validators import validate_float, validate_int


class IntegrationPage(BasePage):
    def __init__(self, parent, **kwargs): super().__init__(parent, **kwargs); self._c1=None; self._build()
    def _build(self):
        ctk.CTkLabel(self, text="∫  Numerical Integration", text_color=ACCENT, font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=20, pady=(18,2))
        self._method=ctk.StringVar(value="Trapezoidal"); tab=ctk.CTkFrame(self, fg_color="transparent"); tab.pack(anchor="w", padx=20)
        for m in ["Trapezoidal","Simpson 1/3","Simpson 3/8"]: ctk.CTkRadioButton(tab,text=m,variable=self._method,value=m,text_color=TEXT_PRI,fg_color=ACCENT).pack(side="left",padx=10)
        content=ctk.CTkFrame(self,fg_color="transparent"); content.pack(fill="both",expand=True,padx=20,pady=8); content.columnconfigure(1,weight=1)
        inp=ctk.CTkFrame(content,fg_color=BG_CARD,corner_radius=12,width=260); inp.grid(row=0,column=0,sticky="ns",padx=(0,12)); inp.grid_propagate(False)
        ctk.CTkLabel(inp,text="Parameters",text_color=ACCENT2,font=ctk.CTkFont(size=14,weight="bold")).pack(anchor="w",padx=14,pady=(14,8))
        for attr,label,default in [("_e_fn","f(x)","x**2"),("_e_a","a","0"),("_e_b","b","1"),("_e_n","n","10")]:
            fr,en=self.labeled_entry(inp,label,default,width=220); fr.pack(padx=14,pady=4,fill="x"); setattr(self,attr,en)
        ctk.CTkButton(inp,text="  ▶  Integrate",height=38,fg_color=ACCENT,text_color="#000000",command=self._solve).pack(padx=14,pady=(16,6),fill="x")
        out=ctk.CTkScrollableFrame(content,fg_color=BG_MAIN); out.grid(row=0,column=1,sticky="nsew"); self._result_lbl=self.make_result_label(out); self._exact_lbl=ctk.CTkLabel(out,text="",text_color=TEXT_SEC); self._exact_lbl.pack(anchor="w",padx=4)
        self._gf=ctk.CTkFrame(out,fg_color=BG_CARD,height=300); self._gf.pack(fill="x",pady=4); self._tbl_card=ctk.CTkFrame(out,fg_color=BG_CARD); self._tbl_card.pack(fill="x",pady=4)
    def _embed(self,fig):
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        if self._c1: self._c1.get_tk_widget().destroy()
        for w in self._gf.winfo_children(): w.destroy()
        c=FigureCanvasTkAgg(fig,master=self._gf); c.draw(); c.get_tk_widget().pack(fill="both",expand=True); self._c1=c
    def _solve(self):
        try:
            f=parse_function(self._e_fn.get()); a=validate_float(self._e_a.get(),"a"); b=validate_float(self._e_b.get(),"b"); n=validate_int(self._e_n.get(),"n",2); method=self._method.get()
            if method=="Trapezoidal": result,xs,ys,table=trapezoidal(f,a,b,n)
            elif method=="Simpson 1/3": result,xs,ys,table=simpson_one_third(f,a,b,n)
            else: result,xs,ys,table=simpson_three_eighth(f,a,b,n)
            self._embed(plot_integration(f,a,b,xs,method)); self.show_table(self._tbl_card,table,max_rows=30)
            try:
                expr,x=get_sympy_expr(self._e_fn.get()); exact=float(sp.integrate(expr,(x,a,b))); err=abs(result-exact)/abs(exact)*100 if exact else 0; self._exact_lbl.configure(text=f"Exact: {exact:.8f} | Approx: {result:.8f} | Error: {err:.4f}%")
            except Exception: self._exact_lbl.configure(text="")
            self.show_result(self._result_lbl,f"OK  Integral ≈ {result:.8f} | Method: {method}")
        except Exception as ex: self.show_result(self._result_lbl,f"Error: {ex}",error=True)
