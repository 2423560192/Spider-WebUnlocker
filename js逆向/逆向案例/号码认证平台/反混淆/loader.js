const fs            = require('fs');
const types         = require("@babel/types");
const parser        = require("@babel/parser");
const traverse      = require("@babel/traverse").default;
const generator     = require("@babel/generator").default;


//js混淆代码读取
process.argv.length > 2 ? encodeFile = process.argv[2]: encodeFile ="./encode.js";
process.argv.length > 3 ? decodeFile = process.argv[3]: decodeFile ="./decode.js";

//将源代码解析为AST
let sourceCode = fs.readFileSync(encodeFile, {encoding: "utf-8"});

let ast    = parser.parse(sourceCode);


console.time("处理完毕，耗时");

const simplifyLiteral = {
	NumericLiteral({node}) {
		if (node.extra && /^0[obx]/i.test(node.extra.raw)) {
			node.extra = undefined;
		}
  },
  StringLiteral({node})
  {
  	if (node.extra && /\\[ux]/gi.test(node.extra.raw)) {
  		node.extra = undefined;
    }
  },
}


traverse(ast,simplifyLiteral);

// 常量函数
var a = function (c, d) {
    var e = "1.1.2";
    function f(g, h) {
      var j = g["length"];
      var l = [];
      for (var m = 0; m < j; m++) {
        var n = h(g[m]);
        l["push"](n);
      }
      return l;
    }
    var p,
      q,
      r,
      s,
      t,
      u = decodeURIComponent,
      v = "Char",
      w = '';
    var x = [a];
    p = "de";
    q = "fr";
    r = "o";
    t = q + r + "m";
    s = "Co" + p;
    var y = function (z) {
      return (z + w)["constructor"][t + v + s](z);
    };
    var A = function (B) {
      return f(B, function (C) {
        return y(C);
      });
    };
    var D = A["call"](y, [39, 34, 37, 96, 60, 120, 97, 65, 98, 66, 99, 67, 100, 68, 101, 69, 102, 70, 103, 110, 109, 111, 112, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]);
    var E = f([28782, 27702, 26416, 25167, 24183], function (p) {
      return u(p);
    });
    var G = A["call"](E, [22354, 22749, 24415, 23346, 22257, 22688, 24306, 25174, 23595, 25547, 22984, 25690, 22212, 27547, 21594, 27210, 23090, 29193, 22394, 29368, 29532, 29459, 29530, 24146, 24500, 26352, 27441, 28788, 29370, 27673, 26925, 25249, 24430]),
      H = {};
    E = A(E);
    var I = new RegExp(E["join"]("|"));
    for (var p = 0; p < D["length"]; p++) {
      H[G[p]] = D[p];
    }
    d = f(d["split"](w), function (K) {
      return H[K] || K;
    })["join"](w);
    return f(d["split"](I), function (p) {
      return u(p);
    });
  }(this, "坺呚t橊l呚獜呚犸t揋yI囄扏i犸犸呚rT呚墠t幷url扏囄廲t廲氶呚rr猓r氶h呚廲囄呚rs扏with摚r呚囄呚犸ti廲ls幷X殛猓獜廲i犸R呚qu呚st灮猓獚呚犸氶獚猓st灮猓犸呚rr猓r扏s呚犸囄朰POST朰猓犸r呚廲囄yst廲t呚姈h廲犸坺呚氶st廲tus氶犸廲獜呚氶t猓Stri犸坺朰j猓i犸氶坺呚t揋猓墠O尫j呚姈t爉猓r朰猓獚呚r廲幷獜廲墠T猓u姈hP猓i犸ts朰獜sM廲墠T猓u姈hP猓i犸ts扏猓犸t猓u姈hst廲rt朰獚r猓囄u姈t灮獚r猓囄u姈tSu尫扏v呚犸囄猓r朰獚l廲t娲猓r獜扏i犸犸呚rWi囄th幷囄猓姈u獜呚犸t橊l呚獜呚犸t朰姈li呚犸tWi囄th扏尫猓囄y氶姈li呚犸tH呚i坺ht灮姈猓l猓r殛呚獚th幷wi囄th朰廲v廲ilWi囄th幷廲v廲ilH呚i坺ht扏囄呚vi姈呚X殛PI幷su尫str氶囄呚s姈ri獚ti猓犸灮l猓姈廲lSt猓r廲坺呚灮i犸囄呚墠呚囄殛揋灮s呚ssi猓犸St猓r廲坺呚灮姈猓猓ki呚橊犸廲尫l呚囄灮坺呚tTi獜呚z猓犸呚O娲娲s呚t氶l廲犸坺u廲坺呚朰l廲犸坺u廲坺呚s朰r呚獚l廲姈呚灮姈r呚廲t呚橊l呚獜呚犸t扏vi囄呚猓彟曰爉猓坺坺彟欱揋彟曰幒姈猓囄呚姈s彟欱殛彟曰曰th呚猓r廲彟曰曰扏vi囄呚猓彟曰爉w呚尫獜彟欱揋彟曰幒姈猓囄呚姈s彟欱殛彟曰曰v獚抡彟曰摚彟曰幒v猓r尫is彟曰曰氶vi囄呚猓彟曰爉w呚尫獜彟欱揋彟曰幒姈猓囄呚姈s彟欱殛彟曰曰v獚彮彟曰曰朰囄呚vi姈呚Pi墠呚lR廲ti猓朰h廲r囄w廲r呚摚猓犸姈urr呚犸姈y扏囄iv灮i犸犸呚rHTML扏彟曰氙犸尫s獚彟欱揋扏廲囄s尫猓墠幷坺呚t橊l呚獜呚犸ts揋y摚l廲ssN廲獜呚扏猓娲娲s呚tH呚i坺ht幷r呚獜猓v呚摚hil囄朰姈廲犸v廲s灮坺呚t摚猓犸t呚墠t幷w呚尫坺l氶坺呚tSu獚獚猓rt呚囄橊墠t呚犸si猓犸s氶坺呚t橊墠t呚犸si猓犸扏坺呚tP廲r廲獜呚t呚r氶UNM扖SK橊殛_R橊N殛橊R橊R_W橊揋GL灮N猓t彟曰幒su獚獚猓rt呚囄灮廲囄囄揋呚h廲vi猓r扏s呚t朰坺呚t揋廲tt呚ry灮姈h廲r坺i犸坺氶囄is姈h廲r坺i犸坺Ti獜呚灮l呚v呚l扏姈ry獚t猓氶囄i坺呚st朰SH扖-徴朰l猓坺灮sqrt朰呚墠獚幷獚猓w朰i犸犸呚r扏l猓姈廲ti猓犸幷猓ri坺i犸灮s獚呚呚姈hSy犸th呚sis扏彟犺揋猓尫j呚姈t彟曰幒氶O尫j呚姈t扏su尫stri犸坺灮sli姈呚幷欱.徴徴.欱扏__廲尫尫廲i囄u_曰幒犺犺_zi囄坺呚t娲灮__廲尫尫廲i囄u_曰幒犺犺_尫i囄坺呚t娲朰__廲尫尫廲i囄u_曰幒犺犺_su尫i囄坺呚t娲灮__廲尫尫廲i囄u_曰幒犺犺_呚墠tr廲_囄廲t廲坺呚t娲朰坺呚tIt呚獜氶MI扖O_LI殛灮us呚r扖坺呚犸t扏r廲犸囄猓獜氶s呚tIt呚獜扏坺呚t幷s獚li姈呚氶姈猓犸姈廲t幷MI扖O_摚S灮w呚尫囄riv呚r灮st猓r呚灮獚呚r獜issi猓犸s灮qu呚ry氶N猓ti娲i姈廲ti猓犸幷st廲t呚幷獚r猓獜獚t灮姈廲llPh廲犸t猓獜幷_獚h廲犸t猓獜幷st廲姈k灮獚h廲犸t猓獜js幷__犸i坺ht獜廲r呚朰_S呚l呚犸iu獜_I殛橊_R呚姈猓r囄呚r幷姈廲llS呚l呚犸iu獜氶_s呚l呚犸iu獜氶姈廲姈h呚_灮囄riv呚r扏_獚l廲ywri坺htR呚姈猓r囄呚rS呚tS呚l呚姈t猓r彟曰幒_獚l廲ywri坺htR呚su獜呚彟曰幒_獚l廲ywri坺htR呚姈猓r囄呚rP呚r娲猓r獜扖姈ti猓犸彟曰幒__獚l廲ywri坺ht_尫i犸囄i犸坺_姈廲ll__彟曰幒_獚l廲ywri坺htR呚姈猓r囄呚rR呚姈猓r囄扖姈ti猓犸彟曰幒_獚l廲ywri坺htR呚姈猓r囄呚rSt廲t呚彟曰幒_獚l廲ywri坺htR呚娲r呚shOv呚rl廲y扏i犸犸呚rH呚i坺ht氶猓ut呚rWi囄th扏R呚坺橊墠獚幷彟犺橊彟犺摚犸彟欱爉娲u犸姈ti猓犸彟曰幒幷彟犺摚(彟犺摚)彟曰幒彟犺摚彟椭揋彟犺摚犸彟欱爉彟犺摚s彟曰揋彟犺摚彟犺揋犸廲tiv呚彟曰幒姈猓囄呚彟犺摚彟犺殛彟犺摚s彟曰揋彟犺摚犸彟欱爉彟犺摚彟椭殛彟犺摚犸彟欱爉彟曰灴灮t猓L猓w呚r摚廲s呚幷t呚st朰姈猓犸t呚犸tWi犸囄猓w灮i娲r廲獜呚氶sr姈囄猓姈灮k呚y扏坺呚tOw犸Pr猓獚呚rty殛呚s姈ri獚t猓r灮廲娲t呚r灮__ivt__灮P呚r獜issi猓犸s朰廲t彟曰幒娲u犸姈ti猓犸T猓Stri犸坺灮Plu坺i犸扖rr廲y幷Mi獜呚Ty獚呚扖rr廲y幷獚lu坺i犸s灮獜i獜呚Ty獚呚s氶坺呚tOw犸Pr猓獚呚rtyN廲獜呚s氶W呚尫GLR呚犸囄呚ri犸坺摚猓犸t呚墠t幷h呚i坺ht幷t猓殛廲t廲URL朰呚墠獚呚ri獜呚犸t廲l-w呚尫坺l朰姈廲犸Pl廲yTy獚呚朰姈猓猓ki呚朰囄呚娲i犸呚Pr猓獚呚rty扏呚v廲l氶橊V扖K_摚扖LL扏HTMLI爉r廲獜呚橊l呚獜呚犸t扏W呚尫GL曰R呚犸囄呚ri犸坺摚猓犸t呚墠t扏欱幒幒幷椭欱_欱幒幒扏椭欱_灴幒徴幷氙幒幒朰椭欱_氙幒幒扏氙幒徴灮坺呚t橊l呚獜呚犸ts揋yT廲坺N廲獜呚灮尫t猓廲扏t呚墠t彟曰爉獚l廲i犸彟欱揋姈h廲rs呚t彟欱殛UT爉-抡朰si囄扏st廲rt幷styl呚扏囄is獚l廲y氶r呚姈t灮isP猓i犸tI犸P廲th灮姈廲犸v廲s彟曰幒wi犸囄i犸坺彟欱扖灮t呚墠t揋廲s呚li犸呚幷廲l獚h廲尫呚ti姈朰彟曰欱娲氙幒扏娲illR呚姈t氶娲illStyl呚扏彟曰欱幒氙彮扏娲猓犸t灮徴徴獚t彟曰幒扖ri廲l灮娲illT呚墠t幷廲犸ti娲r廲u囄氶r坺尫廲(徴幒曰彟曰摚彟曰幒曰幒灴彟曰摚彟曰幒幒彟曰摚彟曰幒幒.曰)幷徴抡獚t彟曰幒扖ri廲l氶坺l猓尫廲l摚猓獜獚猓sit呚O獚呚r廲ti猓犸灮r坺尫(曰犺犺彟曰摚幒彟曰摚曰犺犺)朰尫呚坺i犸P廲th幷廲r姈朰姈l猓s呚P廲th氶r坺尫(幒彟曰摚曰犺犺彟曰摚曰犺犺)氶r坺尫(曰犺犺彟曰摚曰犺犺彟曰摚幒)灮呚v呚犸猓囄囄扏姈廲犸v廲s彟曰幒娲獚彟欱扖朰呚犸囄扏幒.幒.幒.幒灮RT摚P呚呚r摚猓犸犸呚姈ti猓犸扏stu犸彟欱扖stu犸.s呚rvi姈呚s.獜猓zill廲.姈猓獜幷猓犸i姈呚姈廲犸囄i囄廲t呚朰姈廲犸囄i囄廲t呚幷姈r呚廲t呚O娲娲呚r朰s呚tL猓姈廲l殛呚s姈ri獚ti猓犸幷s囄獚扏娲猓r橊廲姈h灮廲彟欱殛姈廲犸囄i囄廲t呚彟欱扖灮姈彟欱殛IN扏囄呚vi姈呚獜猓ti猓犸幷坺呚t殛廲t廲氶htt獚s彟欱扖彟曰爉彟曰爉獜i廲猓.尫廲i囄u.姈猓獜彟曰爉廲尫囄r彟欱爉囄廲t廲彟欱殛灮娲r猓獜摚h廲r摚猓囄呚扏獜i廲猓wu扏i犸it幷i犸it殛廲t廲氶呚墠tr廲殛廲t廲扏su尫i囄幷i犸it扖姈tiv呚殛廲t廲灮r呚獚猓rt幷su姈姈呚ss扏揋摚廲t幷犸廲vi坺廲t猓r扏s姈r呚呚犸氶爉u犸姈ti猓犸氶姈r呚廲t呚灮呚墠t呚犸囄幷姈呚il朰姈l猓犸呚氶姈h廲r摚猓囄呚扖t幷M廲l娲猓r獜呚囄彟曰幒UT爉-抡彟曰幒囄廲t廲氶尫l猓姈kSiz呚氶姈h廲r扖t朰扖揋摚殛橊爉GHIJKLMNOPQRSTUVWXYZ廲尫姈囄呚娲坺hijkl獜犸猓獚qrstuvw墠yz幒徴曰欱灴犺氙椭抡彮彟曰揋彟曰爉彟欱殛幷獜猓囄呚朰獚廲囄囄i犸坺幷娲猓r獜廲t幷stri犸坺幷r呚s呚t灮呚犸姈ry獚t灮囄呚姈ry獚t氶u獚囄廲t呚扏__彟曰灴廲尫呚扏__彟曰灴廲尫囄灮娲l猓猓r灮T呚墠t橊犸姈猓囄呚r灮Ui犸t抡扖rr廲y朰su尫tl呚朰廲姈猓sh氶廲t廲犸h朰廲t廲犸氶si犸h朰姈猓sh氶t廲犸灮t廲犸h扏呚墠獚獜徴扏l猓坺徴獚氶廲尫猓ut彟欱扖尫l廲犸k朰URL朰尫i呚l扏姈猓囄呚s灮尫呚娲猓r呚S呚t幷廲娲t呚rS呚t灮s呚t彟曰幒獜ulti獚l呚彟曰幒娲i呚l囄彟曰幒娲u犸姈ti猓犸彟曰幒廲r坺u獜呚犸ts彟曰幒l呚犸坺th彟曰幒獜ust彟曰幒坺t彟曰幒幒灮犸u獜尫呚r扏s呚tMult彟曰幒姈廲ll尫廲姈k彟曰幒廲r坺u獜呚犸ts彟曰幒姈猓u犸t彟曰幒獜ust彟曰幒呚q彟曰幒s呚t彟曰幒娲i呚l囄彟曰幒姈猓u犸t.幷s呚t彟曰幒獜ult彟曰幒娲i呚l囄彟曰幒廲尫犸猓r獜廲l幷N廲N氶娲i呚l囄彟曰幒朰坺呚t彟曰幒獜ulti獚l呚彟曰幒娲i呚l囄彟曰幒娲u犸姈ti猓犸彟曰幒廲r坺u獜呚犸ts彟曰幒l呚犸坺th彟曰幒獜ust彟曰幒坺t彟曰幒徴灮姈猓獜獚呚l呚囄扏尫呚娲猓r呚摚猓獜獚呚l呚幷彟曰幒st廲tus彟曰幒廲尫犸猓r獜廲l氶猓獚r朰s廲娲廲ri幷S橊彟曰幒曰.X彟曰幒M呚t廲Sr彟曰幒徴.幒幷QQ揋r猓ws呚r幷獜i犸i獚r猓坺r廲獜氶呚v廲lu廲t呚彟灴幒朰姈廲ll爉u犸姈ti猓犸O犸彟灴幒氶呚v廲lu廲t呚彟灴幒囄呚尫u坺坺呚r扏v獚犸_坺呚t_猓尫j扏v獚犸_娲犸_姈廲ll扏廲rs朰尫廲r姈氶尫呚r姈扏尫姈r姈朰獜猓us呚獜猓v呚幷姈li呚犸tY朰r猓t廲ti猓犸R廲t呚朰坺廲獜獜廲灮ty獚呚幷姈li呚犸tX氶獚廲坺呚X幷犸猓囄呚Ty獚呚氶獚廲r呚犸tN猓囄呚幷h廲s扖ttri尫ut呚灮u犸shi娲t氶i囄(彟曰曰氶坺呚t扖ttri尫ut呚幷l猓姈廲lN廲獜呚扏彟犺揋彟灴幒姈l廲ss彟欱殛彟曰曰灮姈l廲ss幷獚r呚vi猓usSi尫li犸坺朰isTrust呚囄朰r呚娲呚rr呚r扏廲犸ti-尫猓t-囄娲幷__廲尫尫廲i囄u_曰幒犺犺_姈i囄姈尫扏__廲尫尫廲i囄u_曰幒徴抡幒欱徴犺_姈i囄姈尫幷__廲尫尫廲i囄u_曰幒犺犺_猓犸呚rr猓r灮獚r猓t猓姈猓l氶h猓st幷__廲尫尫廲i囄u_曰幒犺犺_廲囄v廲犸姈呚囄幷獚r猓t猓ty獚呚朰v廲lu呚幷猓尫j呚姈t扏M廲th灮摚廲犸犸猓t彟曰幒娲i犸囄彟曰幒坺l猓尫廲l彟曰幒猓尫j呚姈t扏s獚lit氶l呚犸坺th氶娲ill氶u犸囄呚娲i犸呚囄扏it呚r廲t猓r朰姈廲ll朰扖rr廲y.娲r猓獜灮娲u犸姈ti猓犸扏犸呚墠t朰獚ush朰獜廲墠扏I犸t抡扖rr廲y.獚r猓t猓ty獚呚.娲ill幷Ui犸t抡摚l廲獜獚呚囄扖rr廲y.獚r猓t猓ty獚呚.娲ill朰I犸t徴氙扖rr廲y.獚r猓t猓ty獚呚.娲ill灮I犸t欱曰扖rr廲y.獚r猓t猓ty獚呚.娲ill幷爉l猓廲t欱曰扖rr廲y.獚r猓t猓ty獚呚.娲ill氶爉l猓廲t氙灴扖rr廲y.獚r猓t猓ty獚呚.娲ill朰Pr猓獜is呚灮r呚j呚姈t扏s呚tTi獜呚猓ut灮摚廲犸犸猓t彟曰幒s呚ttl呚(朰摚ust猓獜橊v呚犸t朰橊v呚犸t扏u犸h廲犸囄l呚囄r呚j呚姈ti猓犸灮囄猓姈u獜呚犸t灮姈r呚廲t呚橊v呚犸t朰i犸it摚ust猓獜橊v呚犸t朰r呚廲s猓犸朰r呚s猓lv呚氶th呚犸扏姈廲t姈h朰U犸呚墠獚呚姈t呚囄彟曰幒st廲t呚彟欱扖彟曰幒朰r廲姈呚扏囄猓犸呚灮廲ssi坺犸朰h廲sOw犸Pr猓獚呚rty幷廲囄囄橊v呚犸tList呚犸呚r朰廲tt廲姈h橊v呚犸t灮r呚獜猓v呚橊v呚犸tList呚犸呚r灮囄呚t廲姈h橊v呚犸t朰坺呚tTi獜呚幷彟犺揋猓尫j呚姈t彟曰幒爉u犸姈ti猓犸彟犺殛朰廲獚獚ly幷r呚廲囄ySt廲t呚氶l猓廲囄幷彟犺揋猓尫j呚姈t彟曰幒Stri犸坺彟犺殛扏stri犸坺i娲y氶獚廲rs呚灮橊幒摚犺灴灴徴徴椭扖扖橊灴爉氙欱幷氙欱氙幒徴灴囄徴椭欱呚幒灴灴幒彮朰娲彮廲彮抡囄灴氙囄灴徴姈灴灴姈囄幷__廲尫尫廲i囄u_曰幒犺犺_姈尫扏__廲尫尫廲i囄u_曰幒徴抡徴曰徴徴_姈尫扏i犸囄呚墠O娲氶__廲尫尫廲i囄u_曰幒徴抡幒欱幒氙_i囄姈尫幷__廲尫尫廲i囄u_曰幒徴抡幒欱徴犺_li囄_s姈猓r呚_姈尫");
  (function (e, f) {
    var g = function (h) {
      while (--h) {
        e['push'](e['shift']());
      }
    };
    g(++f);
  })(a, 306);
  var b = function (d, e) {
    d = d - 0;
    var f = a[d];
    return f;
  };
function isNodeLiteral(node) {//判断形参是否全部为字面量，要不然eval的时候会报错
    if (Array.isArray(node)) {
        return node.every(ele => isNodeLiteral(ele));
    }
    if (types.isLiteral(node)) {
    	if (node.value == null)
    	{
    		return false;
    	}
      return true;
    }
    if(types.isBinaryExpression(node))
    {
    	return isNodeLiteral(node.left) && isNodeLiteral(node.right);
    }
    if (types.isUnaryExpression(node, {
        "operator": "-"
    }) || types.isUnaryExpression(node, {
        "operator": "+"
    })) {
        return isNodeLiteral(node.argument);
    }

    if (types.isObjectExpression(node)) {
        let { properties } = node;
        if (properties.length == 0) {
            return true;
        }

        return properties.every(property => isNodeLiteral(property));

    }
    if (types.isArrayExpression(node)) {
        let { elements } = node;
        if (elements.length == 0) {
            return true;
        }
        return elements.every(element => isNodeLiteral(element));
    }

    return false;
}

let funcNames = ["b"]; //填写函数名。

const callToString = {
    "CallExpression"(path) {
        let node = path.node;

        let {callee, arguments} = node;
        if (!types.isIdentifier(callee) || !funcNames.includes(callee.name))
        {
            return;
        }

        if (arguments.length == 0 || !isNodeLiteral(arguments)) {
            return;
        }

        let value = eval(path.toString());
        console.log(path.toString(), "-->", value);
        path.replaceWith(types.valueToNode(value));
    },
}

traverse(ast, callToString);

console.timeEnd("处理完毕，耗时");


let {code} = generator(ast);

fs.writeFile(decodeFile, code, (err) => {});