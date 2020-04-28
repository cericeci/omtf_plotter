import pickle 
import math 
import ROOT 

pileups = [140, 200, 250, 300]
qualities = ['_q12','_q4','_q0'] 


ROOT.gROOT.ProcessLine('.L PlotTemplate.C+')
ROOT.gROOT.SetBatch(True)

bins=[0.,1.,2.,3.,4.,4.5,5.,6.,7.,8.,10.,12.,14.,16.,18.,20.,25.,30.,35.,40.,45.,50.,60.,70.,80.,90.,100.,120.,140.,200.]

with open('tdr_rates_pu.pickle', 'rb') as handle:
    bb = pickle.load(handle)

theFile = ROOT.TFile("tdr_rates_pu.root","RECREATE")
theFile.cd()

xs = [300,250,200,140] # ,45]
ys = [] 
ye = []
hp = ROOT.TH1F('hp','',1,-0.5,0.5)
ht = ROOT.TH1F('ht','',1,-0.5,0.5)

coeff = 2760.*11.246
for i in range(len(bins)):
  for q in qualities:
    j = 0
    gr = ROOT.TGraphAsymmErrors(5)
    grall = ROOT.TGraphAsymmErrors(7)
    gr.SetPoint(1,0,0)
    grall.SetPoint(1,0,0)
    for pValue in pileups :
      j += 1
      puHandle = ''
      if pValue == 0: puHandle ='NOPU'
      else: puHandle = 'PU' + str(pValue)
      hp.SetBinContent(1, bb['Nu_' + puHandle]['fired'+str(bins[i])+ q] )
      ht.SetBinContent(1, bb['Nu_' + puHandle]['total'] ) 
      eff = ROOT.TEfficiency(hp, ht)
      val    = coeff * eff.GetEfficiency(1)
      val_up = coeff * eff.GetEfficiencyErrorUp(1)
      val_dn = coeff * eff.GetEfficiencyErrorLow(1)
      print pValue, val
      gr.SetPoint(j, pValue,  val)
      gr.SetPointEYlow(j, val_dn)
      gr.SetPointEYhigh(j, val_up)
      
      grall.SetPoint(j, pValue,  val)
      grall.SetPointEYlow(j, val_dn)
      grall.SetPointEYhigh(j, val_up)
 
    canvas = ROOT.CreateCanvas('name',False,True)
    gr.SetMarkerColor(ROOT.kBlack)
    gr.SetLineColor(ROOT.kBlack)
    gr.SetMarkerStyle(8)
    gr.SetTitle("")
    gr.Draw("AP")
    gr.GetXaxis().SetLimits(0,350)
    gr.GetHistogram().SetMaximum(25)
    gr.GetHistogram().SetMinimum(0)
    gr.GetXaxis().SetTitle("Average PU")
    gr.GetYaxis().SetTitle("Rate [kHz]")
    leg = ROOT.TLegend(0.25,0.6,0.55,0.8)
    leg.SetTextSize(0.040)
    leg.SetHeader("p_{T}^{L1} #geq %i GeV"%bins[i])
    leg.AddEntry( gr , "Phase II", 'P')

    if bins[i] == 25:
      # For 25 GeV we have the data points from Marcin
      gr3 = ROOT.TGraphAsymmErrors(2)
      gr3.SetPoint(0, 50, 2.4*0.97)
      gr3.SetPoint(1, 107, 5.7*0.97)
      grall.SetPoint(0, 50, 2.4*0.97)
      grall.SetPoint(1, 107, 5.7*0.97)

      gr3.SetMarkerStyle(22)
      gr3.SetMarkerSize(2)
      gr3.SetMarkerColor(ROOT.kBlue)
      gr3.SetLineColor(ROOT.kBlue)
      gr3.Draw("P SAME")
      gr3.SetName("data_rates_pu_pt%i_%s"%(bins[i], q))
      gr3.Write()
      leg.AddEntry( gr3, "2018 Data", 'EP')
      fun = ROOT.TF1('f','[0]*x',0,350)
      grall.Fit('f')
      print fun.GetParameter(0), '+/-', fun.GetParError(0)
      fun.Draw("same")


    else:
      # For other pT only show points + fit
      fun = ROOT.TF1('f','[0]*x',0,350)
      gr.Fit('f')
      print fun.GetParameter(0), '+/-', fun.GetParError(0)
      fun.Draw("same")
    gr.SetName("mc_rates_pu_pt%i_%s"%(bins[i], q))
    gr.Write()
    fun.SetName("fit_pu_pt%i_%s"%(bins[i],q) )
    fun.Write()
    leg.AddEntry( fun, "Linear fit")
    leg.Draw()
    ROOT.DrawPrelimLabel(canvas)
    ROOT.DrawLumiLabel(canvas,'14 TeV')
    ROOT.SaveCanvas(canvas,'omtf_tdr_pu_rate_q'+ q + "_pt%i"%bins[i])
theFile.Close()
